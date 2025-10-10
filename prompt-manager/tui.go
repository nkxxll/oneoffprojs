package main

import (
	"fmt"
	"log/slog"
	"os"
	"strings"

	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/list"
	"github.com/charmbracelet/bubbles/textarea"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
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
	text string
}

func (i item) FilterValue() string { return i.name + " " + i.text + " " + strings.Join(i.tags, " ") }
func (i item) Title() string       { return i.name }
func (i item) Description() string { return "" }

// NewTUI creates a new TUI model.
func NewTUI(target string) (*tuiModel, error) {
	store, err := NewStore()
	if err != nil {
		return nil, err
	}

	var items []list.Item
	for _, p := range store.GetAll() {
		items = append(items, item{id: p.ID, name: p.Name, tags: p.Tags, text: p.Text})
	}

	delegate := list.NewDefaultDelegate()
	l := list.New(items, delegate, 20, 14)
	l.Title = "Your Prompts"

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
	f, err := tea.LogToFile("debug.log", "debug")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer f.Close()

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
	var cmds []tea.Cmd
	var cmd tea.Cmd
	var quit bool

	slog.Info(fmt.Sprintf("Filtering state %v", m.list.FilterState()))
	slog.Info(fmt.Sprintf("Filtering value %v", m.list.FilterValue()))
	slog.Info(fmt.Sprintf("Filtering items %v", m.list.Items()))

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.list.SetWidth(msg.Width)
		m.list.SetHeight(msg.Height)
		if m.form != nil {
			m.form.text.SetWidth(msg.Width)
		}
	}

	switch m.state {
	case listView:
		quit, cmd = m.updateListView(msg)
		// TODO yes this is a war crime but I dont want to make it nice I want
		// to make it work this is because you cannot use batch with quit
		// because of race conditions the program ends but one thread might be still
		// running
		if quit {
			return m, tea.Quit
		}
		cmds = append(cmds, cmd)

		m.list, cmd = m.list.Update(msg)
		cmds = append(cmds, cmd)

	case formView:
		cmd = m.updateFormView(msg)
		cmds = append(cmds, cmd)

		var nameCmd, textCmd, tagsCmd tea.Cmd
		m.form.name, nameCmd = m.form.name.Update(msg)
		m.form.text, textCmd = m.form.text.Update(msg)
		m.form.tags, tagsCmd = m.form.tags.Update(msg)
		cmds = append(cmds, nameCmd, textCmd, tagsCmd)

		for i := 0; i <= 2; i++ {
			if i == m.form.focusIndex {
				cmds = append(cmds, m.form.Focus(i))
			} else {
				m.form.Blur(i)
			}
		}
	}

	return m, tea.Batch(cmds...)
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

func (m *tuiModel) updateListView(msg tea.Msg) (quit bool, cmd tea.Cmd) {
	keyMsg, ok := msg.(tea.KeyMsg)
	quit = false
	cmd = nil
	if !ok {
		return
	}

	if m.list.FilterState() == list.Filtering {
		return
	}

	switch {
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("q", "ctrl+c"))):
		m.quitting = true
		return true, tea.Quit
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("enter"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			p, found := m.store.Get(i.id)
			if found {
				Send(m.tmuxTarget, p.Text, false)
				m.quitting = true
				return true, tea.Quit
			}
		}
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("c"))):
		m.state = formView
		m.form = NewCreateForm()
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("e"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			p, found := m.store.Get(i.id)
			if found {
				m.state = formView
				m.form = NewEditForm(p)
			}
		}
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("d"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			m.store.Remove(i.id)
			m.list.RemoveItem(m.list.Index())
		}
	}
	return
}

func (m *tuiModel) updateFormView(msg tea.Msg) tea.Cmd {
	keyMsg, ok := msg.(tea.KeyMsg)
	if !ok {
		return nil
	}

	switch {
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("esc"))):
		m.state = listView
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("enter"))):
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
				items = append(items, item{id: pr.ID, name: pr.Name, tags: pr.Tags, text: pr.Text})
			}
			m.list.SetItems(items)
			m.state = listView
		} else {
			m.form.focusIndex = (m.form.focusIndex + 1) % 3
		}
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("tab"))):
		m.form.focusIndex = (m.form.focusIndex + 1) % 3
	}
	return nil
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
	name.Width = 50

	text := textarea.New()
	text.Placeholder = "Prompt Text"
	text.SetWidth(50)

	tags := textinput.New()
	tags.Placeholder = "tag1,tag2,tag3"
	tags.Width = 50

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
