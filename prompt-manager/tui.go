package main

import (
	"fmt"
	"io"
	"log"
	"log/slog"
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
	templateView
)

// tuiModel is the main model for the TUI.
type tuiModel struct {
	store         *Store
	list          list.Model
	form          *Form
	templateForm  *TemplateForm
	state         viewState
	err           error
	tmuxTarget    string
	quitting      bool
	terminalWidth int
}

// Form represents the create/edit form.
type Form struct {
	id         *uuid.UUID
	name       textinput.Model
	text       textarea.Model
	tags       textinput.Model
	focusIndex int
}

// TemplateForm represents the form for filling in template fields.
type TemplateForm struct {
	inputs     []textinput.Model
	focusIndex int
	promptText string
	promptName string
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
	log.SetOutput(io.Discard)
	// f, err := tea.LogToFile("debug.log", "debug")
	// if err != nil {
	// 	fmt.Println(err)
	// 	os.Exit(1)
	// }
	// defer f.Close()

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

	slog.Info(fmt.Sprintf("State: %v, Filtering state %v", m.state, m.list.FilterState()))

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.list.SetWidth(msg.Width)
		m.list.SetHeight(msg.Height)
		m.terminalWidth = msg.Width
		if m.form != nil {
			m.form.text.SetWidth(msg.Width / 2)
		}
	}

	switch m.state {
	case listView:
		quit, cmd = m.updateListView(msg)
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
	case templateView:
		quit, cmd = m.updateTemplateView(msg)
		if quit {
			return m, tea.Quit
		}
		cmds = append(cmds, cmd)

		// templateForm is nil if we escape from the form
		if m.templateForm != nil {
			// Update all text inputs
			newInputs := make([]textinput.Model, len(m.templateForm.inputs))
			for i := range m.templateForm.inputs {
				var inputCmd tea.Cmd
				newInputs[i], inputCmd = m.templateForm.inputs[i].Update(msg)
				cmds = append(cmds, inputCmd)
			}
			m.templateForm.inputs = newInputs

			// Set focus
			for i := range m.templateForm.inputs {
				if i == m.templateForm.focusIndex {
					cmds = append(cmds, m.templateForm.inputs[i].Focus())
				} else {
					m.templateForm.inputs[i].Blur()
				}
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
	case templateView:
		return m.templateForm.View()
	default:
		return ""
	}
}

func (m *tuiModel) updateListView(msg tea.Msg) (quit bool, cmd tea.Cmd) {
	keyMsg, ok := msg.(tea.KeyMsg)
	quit = false
	cmd = nil
	if !ok {
		return quit, cmd
	}

	if m.list.FilterState() == list.Filtering {
		return quit, cmd
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
				fields := ParseTemplate(p.Text)
				if len(fields) == 0 {
					Send(m.tmuxTarget, p.Text, false)
					m.quitting = true
					return true, tea.Quit
				}

				// Has template fields, switch to template view
				m.state = templateView
				m.templateForm = NewTemplateForm(p.Name, p.Text, fields, m.terminalWidth)
				return false, m.templateForm.Init()
			}
		}
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("c"))):
		m.state = formView
		m.form = NewCreateForm(m.terminalWidth)
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("e"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			p, found := m.store.Get(i.id)
			if found {
				m.state = formView
				m.form = NewEditForm(p, m.terminalWidth)
			}
		}
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("d"))):
		i, ok := m.list.SelectedItem().(item)
		if ok {
			m.store.Remove(i.id)
			m.list.RemoveItem(m.list.Index())
		}
	}
	return quit, cmd
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

func (m *tuiModel) updateTemplateView(msg tea.Msg) (bool, tea.Cmd) {
	keyMsg, ok := msg.(tea.KeyMsg)
	if !ok {
		return false, nil
	}

	switch {
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("esc"))):
		m.state = listView
		m.templateForm = nil
		return false, nil
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("enter"))):
		if m.templateForm.focusIndex == len(m.templateForm.inputs)-1 {
			// Last field, render and quit
			values := make(map[string]string)
			for _, input := range m.templateForm.inputs {
				// The placeholder is the key
				values[input.Placeholder] = input.Value()
			}
			rendered := RenderTemplate(m.templateForm.promptText, values)
			Send(m.tmuxTarget, rendered, false)
			m.quitting = true
			return true, tea.Quit
		}
		// Move to next input
		m.templateForm.focusIndex++
		return false, nil
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("tab"))):
		m.templateForm.focusIndex = (m.templateForm.focusIndex + 1) % len(m.templateForm.inputs)
		return false, nil
	case key.Matches(keyMsg, key.NewBinding(key.WithKeys("shift+tab"))):
		m.templateForm.focusIndex--
		if m.templateForm.focusIndex < 0 {
			m.templateForm.focusIndex = len(m.templateForm.inputs) - 1
		}
		return false, nil
	}
	return false, nil
}

// Form methods
func NewCreateForm(terminalWidth int) *Form {
	return newForm(nil, terminalWidth)
}

func NewEditForm(p Prompt, terminalWidth int) *Form {
	form := newForm(&p.ID, terminalWidth)
	form.name.SetValue(p.Name)
	form.text.SetValue(p.Text)
	form.tags.SetValue(strings.Join(p.Tags, ","))
	return form
}

func newForm(id *uuid.UUID, terminalWidth int) *Form {
	name := textinput.New()
	name.Placeholder = "Prompt Name"
	name.Focus()
	name.Width = terminalWidth / 2

	text := textarea.New()
	text.Placeholder = "Prompt Text"
	text.SetWidth(terminalWidth / 2)

	tags := textinput.New()
	tags.Placeholder = "tag1,tag2,tag3"
	tags.Width = terminalWidth / 2

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

// TemplateForm methods
func NewTemplateForm(promptName, promptText string, fields []string, terminalWidth int) *TemplateForm {
	inputs := make([]textinput.Model, len(fields))
	for i, field := range fields {
		inputs[i] = textinput.New()
		inputs[i].Placeholder = field
		inputs[i].CharLimit = 128
		inputs[i].Width = terminalWidth / 2
		if i == 0 {
			inputs[i].Focus()
		}
	}

	return &TemplateForm{
		inputs:     inputs,
		promptName: promptName,
		promptText: promptText,
		focusIndex: 0,
	}
}

func (f *TemplateForm) Init() tea.Cmd {
	return textinput.Blink
}

func (f *TemplateForm) View() string {
	var b strings.Builder
	b.WriteString(lipgloss.NewStyle().Bold(true).Render("Fill in template for: " + f.promptName))
	b.WriteString("\n\n")

	b.WriteString(lipgloss.NewStyle().Bold(true).Render(f.promptText))
	b.WriteString("\n\n")

	for i := range f.inputs {
		b.WriteString(f.inputs[i].View())
		if i < len(f.inputs)-1 {
			b.WriteString("\n")
		}
	}

	b.WriteString("\n\nEnter to confirm, Esc to cancel, Tab to navigate")
	return b.String()
}
