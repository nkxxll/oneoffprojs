#let project(title: "", authors: (), date: none, body) = {
  set document(author: authors, title: title)
  set page(
    margin: (left: 25mm, right: 25mm, top: 25mm, bottom: 25mm),
    numbering: "1 / 1",
    number-align: center,
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: luma(100))
        #title
        #h(1fr)
        #if date != none { date }
        #line(length: 100%, stroke: 0.5pt + luma(180))
      ]
    },
  )
  set text(font: "Libertinus Serif", lang: "en", size: 10.5pt)
  set heading(numbering: "1.1")
  
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(1em)
    block(text(weight: 700, 1.2em, it))
    v(0.5em)
  }
  
  show heading.where(level: 2): it => {
    v(0.8em)
    block(text(weight: 600, 1.1em, it))
    v(0.3em)
  }
  
  show raw.where(block: true): it => {
    set text(size: 9pt)
    block(
      fill: luma(245),
      stroke: 0.5pt + luma(200),
      inset: 10pt,
      radius: 3pt,
      width: 100%,
      it
    )
  }
  
  show raw.where(block: false): it => {
    box(
      fill: luma(240),
      inset: (x: 3pt, y: 0pt),
      outset: (y: 3pt),
      radius: 2pt,
      text(size: 9pt, it)
    )
  }
  
  // Title block
  align(center)[
    #v(2em)
    #block(text(weight: 700, 1.75em, title))
    #v(1em, weak: true)
    #if authors != () and authors.len() > 0 {
      let author-text = if type(authors) == str { authors } else { authors.join(", ") }
      text(0.95em, author-text)
      v(0.5em)
    }
    #if date != none {
      text(0.9em, style: "italic", date)
    }
    #v(3em, weak: true)
  ]
  
  // Table of contents for longer docs
  outline(
    title: [Contents],
    indent: 1.5em,
    depth: 3,
  )
  pagebreak()

  // Main body
  set par(justify: true, leading: 0.65em)
  body
}

#show: project.with(
  title: "$title$",
  authors: ($for(author)$"$author$"$sep$, $endfor$),
  date: "$date$",
)

$body$
