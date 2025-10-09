package main

import (
	"fmt"
	"io"
	"strings"

	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/list"
	"github.com/charmbracelet/bubbles/textarea"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/google/uuid"
)

type viewState int

const (
	listView viewState = iota
	formView
)

// tuiModel is the main model for the TUI.
type tuiModel struct {
	store      *Store
	list       list.Model
	form       *Form
	state      viewState
	err        error
	tmuxTarget string
	quitting   bool
}

// Form represents the create/edit form.
type Form struct {
	id         *uuid.UUID
	name       textinput.Model
	text       textarea.Model
	tags       textinput.Model
	focusIndex int
}

// item represents a list item.
type item struct {
	id   uuid.UUID
	name string
	tags []string
}

func (i item) FilterValue() string { return i.name }
func (i item) Title() string       { return i.name }
func (i item) Description() string { return strings.Join(i.tags, ", ") }

// itemDelegate is the delegate for the list component.
type itemDelegate struct{}

func (d itemDelegate) Height() int                               { return 1 }
func (d itemDelegate) Spacing() int                              { return 0 }
func (d itemDelegate) Update(msg tea.Msg, m *list.Model) tea.Cmd { return nil }
func (d itemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	i, ok := listItem.(item)
	if !ok {
		return
	}

	str := fmt.Sprintf("%s", i.name)

	fn := lipgloss.NewStyle().PaddingLeft(4).Render
	if index == m.Index() {
		fn = func(s ...string) string {
			return lipgloss.NewStyle().PaddingLeft(2).Foreground(lipgloss.Color("170")).Render("> " + strings.Join(s, " "))
		}
	}

	fmt.Fprint(w, fn(str))
}

// NewTUI creates a new TUI model.
func NewTUI(target string) (*tuiModel, error) {
	store, err := NewStore()
	if err != nil {
		return nil, err
	}

	var items []list.Item
	for _, p := range store.GetAll() {
		items = append(items, item{id: p.ID, name: p.Name, tags: p.Tags})
	}

	l := list.New(items, itemDelegate{}, 20, 14)
	l.Title = "Your Prompts"
	l.SetShowStatusBar(false)
	l.SetFilteringEnabled(true)
	l.Styles.Title = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	l.Styles.PaginationStyle = list.DefaultStyles().PaginationStyle.PaddingLeft(4)
	l.Styles.HelpStyle = list.DefaultStyles().HelpStyle.PaddingLeft(4).PaddingBottom(1)

	l.AdditionalShortHelpKeys = func() []key.Binding {
		return []key.Binding{
			key.NewBinding(key.WithKeys("enter"), key.WithHelp("enter", "select")),
			key.NewBinding(key.WithKeys("c"), key.WithHelp("c", "create")),
			key.NewBinding(key.WithKeys("e"), key.WithHelp("e", "edit")),
			key.NewBinding(key.WithKeys("d"), key.WithHelp("d", "delete")),
		}
	}

	return &tuiModel{
		store:      store,
		list:       l,
		tmuxTarget: target,
		state:      listView,
	}, nil
}

// RunTUI starts the TUI.
func RunTUI(targetPane string) error {
	if !IsTmuxAvailable() {
		return fmt.Errorf("tmux command not found")
	}

	m, err := NewTUI(targetPane)
	if err != nil {
		return err
	}

	p := tea.NewProgram(m, tea.WithAltScreen())
	_, err = p.Run()
	return err
}

func (m *tuiModel) Init() tea.Cmd {
	return nil
}

func (m *tuiModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.list.SetWidth(msg.Width)
		return m, nil

	case tea.KeyMsg:
		switch m.state {
		case listView:
			return m.updateListView(msg)
		case formView:
			return m.updateFormView(msg)
		}
	}

	return m, cmd
}

func (m *tuiModel) View() string {
	if m.quitting {
		return ""
	}
	switch m.state {
	case listView:
		return m.list.View()
	case formView:
		return m.form.View()
	default:
		return ""
	}
}

func (m *tuiModel) updateListView(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	if m.list.FilterState() == list.Filtering {
		var cmd tea.Cmd
		m.list, cmd = m.list.Update(msg)
		return m, cmd
	}

	switch {
	case key.Matches(msg, key.NewBinding(key.WithKeys("q", "ctrl+c"))):
		m.quitting = true
		return m, tea.Quit
	case key.Matches(msg, key.NewBinding(key.WithKeys("enter"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			p, found := m.store.Get(i.id)
			if found {
				Send(m.tmuxTarget, p.Text, true)
				m.quitting = true
				return m, tea.Quit
			}
		}
		return m, nil
	case key.Matches(msg, key.NewBinding(key.WithKeys("c"))):
		m.state = formView
		m.form = NewCreateForm()
		return m, nil
	case key.Matches(msg, key.NewBinding(key.WithKeys("e"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			p, found := m.store.Get(i.id)
			if found {
				m.state = formView
				m.form = NewEditForm(p)
				return m, nil
			}
		}
		return m, nil
	case key.Matches(msg, key.NewBinding(key.WithKeys("d"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			m.store.Remove(i.id)
			m.list.RemoveItem(m.list.Index())
		}
		return m, nil
	}

	var cmd tea.Cmd
	m.list, cmd = m.list.Update(msg)
	return m, cmd
}

func (m *tuiModel) updateFormView(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch {
	case key.Matches(msg, key.NewBinding(key.WithKeys("esc"))):
		m.state = listView
		return m, nil
	case key.Matches(msg, key.NewBinding(key.WithKeys("enter"))):
		if m.form.focusIndex == 2 { // On tags input
			// Save logic
			p := Prompt{
				Name: m.form.name.Value(),
				Text: m.form.text.Value(),
				Tags: strings.Split(m.form.tags.Value(), ","),
			}
			if m.form.id != nil { // Update
				p.ID = *m.form.id
				m.store.Update(p)
			} else { // Create
				p.ID = uuid.New()
				m.store.Add(p)
			}
			// Refresh list
			var items []list.Item
			for _, pr := range m.store.GetAll() {
				items = append(items, item{id: pr.ID, name: pr.Name, tags: pr.Tags})
			}
			m.list.SetItems(items)
			m.state = listView
		} else {
			m.form.focusIndex = (m.form.focusIndex + 1) % 3
		}
	case key.Matches(msg, key.NewBinding(key.WithKeys("tab"))):
		m.form.focusIndex = (m.form.focusIndex + 1) % 3
	}

	cmds := make([]tea.Cmd, 3)
	m.form.name, cmds[0] = m.form.name.Update(msg)
	m.form.text, cmds[1] = m.form.text.Update(msg)
	m.form.tags, cmds[2] = m.form.tags.Update(msg)

	for i := 0; i <= 2; i++ {
		if i == m.form.focusIndex {
			cmds[i] = m.form.Focus(i)
		} else {
			m.form.Blur(i)
		}
	}

	return m, tea.Batch(cmds...)
}

// Form methods
func NewCreateForm() *Form {
	return newForm(nil)
}

func NewEditForm(p Prompt) *Form {
	form := newForm(&p.ID)
	form.name.SetValue(p.Name)
	form.text.SetValue(p.Text)
	form.tags.SetValue(strings.Join(p.Tags, ","))
	return form
}

func newForm(id *uuid.UUID) *Form {
	name := textinput.New()
	name.Placeholder = "Prompt Name"
	name.Focus()

	text := textarea.New()
	text.Placeholder = "Prompt Text"

	tags := textinput.New()
	tags.Placeholder = "tag1,tag2,tag3"

	return &Form{
		id:         id,
		name:       name,
		text:       text,
		tags:       tags,
		focusIndex: 0,
	}
}

func (f *Form) Focus(i int) tea.Cmd {
	switch i {
	case 0:
		return f.name.Focus()
	case 1:
		return f.text.Focus()
	case 2:
		return f.tags.Focus()
	}
	return nil
}

func (f *Form) Blur(i int) {
	switch i {
	case 0:
		f.name.Blur()
	case 1:
		f.text.Blur()
	case 2:
		f.tags.Blur()
	}
}

func (f *Form) View() string {
	var b strings.Builder
	b.WriteString("Enter to confirm, Esc to cancel\n\n")
	b.WriteString(f.name.View())
	b.WriteString("\n")
	b.WriteString(f.text.View())
	b.WriteString("\n")
	b.WriteString(f.tags.View())
	return b.String()
}
