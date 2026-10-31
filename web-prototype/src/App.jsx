import { useEffect, useMemo, useState } from 'react'
import { Link, NavLink, Route, Routes, useNavigate } from 'react-router-dom'

const THEME_ORDER = ['Claim Status', 'Document Upload', 'Document Requirements', 'Customer Support', 'Login & Access', 'Reimbursement', 'General Experience']
const SEVERITY_ORDER = ['None', 'Low', 'Medium', 'High']
const SENTIMENT_ORDER = ['Negative', 'Neutral', 'Positive']

function parseCsv(text) {
  const rows = []
  let row = [], value = '', quoted = false
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i], next = text[i + 1]
    if (char === '"' && quoted && next === '"') { value += '"'; i += 1 }
    else if (char === '"') quoted = !quoted
    else if (char === ',' && !quoted) { row.push(value); value = '' }
    else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && next === '\n') i += 1
      row.push(value); value = ''
      if (row.some((cell) => cell !== '')) rows.push(row)
      row = []
    } else value += char
  }
  if (value || row.length) { row.push(value); rows.push(row) }
  const [headers, ...data] = rows
  return data.map((cells) => Object.fromEntries(headers.map((header, index) => [header.trim(), (cells[index] ?? '').trim()])))
}

const countBy = (records, field) => records.reduce((acc, record) => ({ ...acc, [record[field]]: (acc[record[field]] || 0) + 1 }), {})
const percent = (part, total) => total ? (part / total) * 100 : 0
const formatPercent = (value) => `${value.toFixed(1)}%`

function useFeedback() {
  const [records, setRecords] = useState([])
  const [error, setError] = useState('')
  useEffect(() => {
    fetch('/customer_feedback_classified.csv')
      .then((response) => { if (!response.ok) throw new Error('Could not load the classified feedback file.'); return response.text() })
      .then((text) => setRecords(parseCsv(text)))
      .catch((err) => setError(err.message))
  }, [])
  return { records, error }
}

function Icon({ name }) {
  const icons = {
    overview: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
    insights: <><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19H2"/></>,
    evidence: <><path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/></>,
    actions: <><path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><circle cx="12" cy="12" r="5"/></>,
    arrow: <><path d="M5 12h14M13 6l6 6-6 6"/></>,
    back: <><path d="M19 12H5M11 18l-6-6 6-6"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
  }
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{icons[name]}</svg>
}

function Layout({ children }) {
  const nav = [
    ['/', 'Overview', 'overview'],
    ['/insights/document-upload', 'Insights', 'insights'],
    ['/evidence/document-upload', 'Evidence', 'evidence'],
    ['/product-action/document-upload', 'Product Actions', 'actions'],
  ]
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand-mark">VoC</div>
      <div className="brand-copy"><strong>Voice of Customer</strong><span>AI Copilot</span></div>
      <nav>{nav.map(([to, label, icon]) => <NavLink key={to} to={to} end={to === '/'}><Icon name={icon}/><span>{label}</span></NavLink>)}</nav>
      <div className="sidebar-principle"><span>Product principle</span><strong>AI assists.</strong><strong>Evidence supports.</strong><strong>PM decides.</strong></div>
      <div className="demo-label">Demo · Synthetic dataset</div>
    </aside>
    <main className="main">{children}</main>
  </div>
}

function PageHeader({ eyebrow, title, subtitle, backTo, backLabel, actions }) {
  return <header className="page-header">
    <div>
      {backTo && <Link className="back-link" to={backTo}><Icon name="back"/>{backLabel}</Link>}
      {eyebrow && <div className="eyebrow">{eyebrow}</div>}
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    {actions && <div className="header-actions">{actions}</div>}
  </header>
}

const Badge = ({ children, tone = 'neutral' }) => <span className={`badge badge-${tone}`}>{children}</span>
const Card = ({ children, className = '' }) => <section className={`card ${className}`}>{children}</section>
const SectionTitle = ({ title, subtitle }) => <div className="section-title"><div><h2>{title}</h2>{subtitle && <p>{subtitle}</p>}</div></div>

function StatCard({ label, value, detail, accent }) {
  return <Card className="stat-card"><div className="stat-top"><span>{label}</span>{accent && <span className="stat-dot"/>}</div><strong>{value}</strong><small>{detail}</small></Card>
}

function LoadingState({ error }) {
  return <div className="loading-state">{error ? <><strong>Unable to load feedback</strong><p>{error}</p></> : <><span className="loader"/><p>Loading classified feedback…</p></>}</div>
}

function ThemeBars({ records }) {
  const counts = countBy(records, 'theme'), max = Math.max(...Object.values(counts))
  return <div className="bar-list">{THEME_ORDER.map((theme) => {
    const count = counts[theme] || 0
    return <div className={`bar-row ${theme === 'Document Upload' ? 'bar-highlight' : ''}`} key={theme}>
      <div className="bar-label"><span>{theme}</span><strong>{count}</strong><small>{formatPercent(percent(count, records.length))}</small></div>
      <div className="bar-track"><span style={{ width: `${(count / max) * 100}%` }}/></div>
    </div>
  })}</div>
}

function Distribution({ records, field, order }) {
  const counts = countBy(records, field)
  return <div className="distribution">
    <div className={`stacked stacked-${field}`}>{order.map((item) => <span key={item} className={`segment segment-${item.toLowerCase()}`} style={{ width: `${percent(counts[item] || 0, records.length)}%` }}/>)}</div>
    <div className="legend">{order.map((item) => <div key={item}><span className={`legend-dot legend-${item.toLowerCase()}`}/><span>{item}</span><strong>{counts[item] || 0}</strong><small>{formatPercent(percent(counts[item] || 0, records.length))}</small></div>)}</div>
  </div>
}

function Overview({ records }) {
  const themeCounts = countBy(records, 'theme'), sentimentCounts = countBy(records, 'sentiment')
  const mediumHigh = records.filter((r) => ['Medium', 'High'].includes(r.severity)).length
  const candidates = ['Document Upload', 'Claim Status', 'Customer Support'].map((theme) => {
    const themeRecords = records.filter((r) => r.theme === theme)
    return { theme, count: themeRecords.length, mediumHigh: themeRecords.filter((r) => ['Medium', 'High'].includes(r.severity)).length }
  })
  return <>
    <PageHeader eyebrow="Feedback intelligence" title="Customer Feedback Overview" subtitle="Understand emerging customer pain points and explore the evidence behind them." actions={<div className="date-chip">Jul 1 – Aug 31, 2026</div>}/>
    <div className="kpi-grid">
      <StatCard label="Feedback Records" value={records.length} detail="July–August 2026" />
      <StatCard label="Themes Identified" value={Object.keys(themeCounts).length} detail={`Across ${records.length} feedback records`} />
      <StatCard label="Negative Feedback" value={sentimentCounts.Negative || 0} detail={`${formatPercent(percent(sentimentCounts.Negative || 0, records.length))} of feedback`} />
      <StatCard label="Medium + High Severity" value={mediumHigh} detail={`${formatPercent(percent(mediumHigh, records.length))} of feedback`} />
    </div>
    <div className="overview-grid">
      <Card className="theme-card"><SectionTitle title="Feedback by Theme" subtitle="Count and share of all 150 feedback records"/><ThemeBars records={records}/></Card>
      <div className="distribution-column">
        <Card><SectionTitle title="Sentiment Distribution" subtitle="Across all feedback records"/><Distribution records={records} field="sentiment" order={SENTIMENT_ORDER}/></Card>
        <Card><SectionTitle title="Severity Distribution" subtitle="Impact described in the feedback"/><Distribution records={records} field="severity" order={SEVERITY_ORDER}/></Card>
      </div>
    </div>
    <Card className="pain-card"><SectionTitle title="Emerging Signals" subtitle="Candidate pain points for PM investigation—not automatic priorities"/>
      <div className="pain-list">{candidates.map((item, index) => <div className={`pain-row ${index === 0 ? 'pain-primary' : ''}`} key={item.theme}>
        <div className="rank">0{index + 1}</div><div className="pain-copy"><div><h3>{item.theme}</h3><Badge tone={index === 0 ? 'blue' : 'neutral'}>{index === 0 ? 'Candidate Pain Point' : 'Emerging Signal'}</Badge></div><p>{item.count} feedback records · {formatPercent(percent(item.count, records.length))} share of feedback · {item.mediumHigh} Medium/High</p></div>
        {index === 0 ? <Link className="button button-primary" to="/insights/document-upload">View Insight <Icon name="arrow"/></Link> : <span className="review-label">Available for review</span>}
      </div>)}</div>
    </Card>
  </>
}

function getDocumentMetrics(records) {
  const docs = records.filter((r) => r.theme === 'Document Upload')
  const monthly = [7, 8].map((month) => {
    const monthRecords = records.filter((r) => new Date(`${r.date}T00:00:00`).getMonth() + 1 === month)
    const count = docs.filter((r) => new Date(`${r.date}T00:00:00`).getMonth() + 1 === month).length
    return { month: month === 7 ? 'July' : 'August', count, total: monthRecords.length, share: percent(count, monthRecords.length) }
  })
  return { docs, negative: docs.filter((r) => r.sentiment === 'Negative').length, mediumHigh: docs.filter((r) => ['Medium', 'High'].includes(r.severity)).length, share: percent(docs.length, records.length), monthly, difference: monthly[1].share - monthly[0].share }
}

function Insight({ records }) {
  const m = getDocumentMetrics(records)
  const evidence = ['F127', 'F021', 'F062'].map((id) => m.docs.find((r) => r.feedback_id === id)).filter(Boolean)
  return <>
    <PageHeader backTo="/" backLabel="Back to Overview" title="Document Upload" subtitle="Why the Copilot surfaced this feedback theme for Product Manager review." actions={<Badge tone="blue">Candidate Pain Point</Badge>}/>
    <div className="trace-strip"><span>AI summary</span><Icon name="arrow"/><span>Supporting metrics</span><Icon name="arrow"/><span>Original customer evidence</span></div>
    <Card className="ai-summary"><div className="ai-title"><span className="ai-mark">AI</span><div><h2>AI Summary</h2><p>Generated from classified feedback · Verify against supporting evidence</p></div></div><blockquote>“Document Upload feedback commonly describes uncertainty about whether submitted files were received or recognized. Some records also describe being asked for documents again after uploading.”</blockquote></Card>
    <div className="kpi-grid insight-kpis">
      <StatCard label="Feedback Records" value={m.docs.length} detail="Document Upload" />
      <StatCard label="Negative" value={m.negative} detail={`${formatPercent(percent(m.negative, m.docs.length))} of theme records`} />
      <StatCard label="Medium / High" value={m.mediumHigh} detail="Impact-based severity" />
      <StatCard label="Share of All Feedback" value={formatPercent(m.share)} detail={`${m.docs.length} of ${records.length} records`} />
    </div>
    <div className="insight-grid">
      <Card><SectionTitle title="Share of Monthly Feedback" subtitle="Record volume and within-month share are shown separately"/><div className="month-chart">{m.monthly.map((month) => <div className="month-column" key={month.month}><div className="month-value">{formatPercent(month.share)}</div><div className="month-bar"><span style={{height:`${(month.share / 30) * 100}%`}}/></div><strong>{month.month}</strong><small>{month.count} of {month.total} records</small></div>)}<div className="month-change"><span>Difference</span><strong>+{m.difference.toFixed(1)} percentage points</strong><small>share of monthly feedback</small></div></div><p className="chart-note">Observation: its share of collected feedback increased. Signal only — further investigation is needed to understand the cause.</p></Card>
      <Card><SectionTitle title="Recurring Patterns" subtitle="Recurring patterns identified across supporting feedback"/><div className="pattern-list">{['Uncertainty about upload confirmation','Repeated document requests after upload','Missing-document messages after upload'].map((pattern) => <div key={pattern}><span><Icon name="check"/></span><p>{pattern}</p></div>)}</div></Card>
    </div>
    <Card><SectionTitle title="Supporting Evidence Preview" subtitle="Original feedback supporting this insight"/><div className="evidence-preview">{evidence.map((record) => <EvidenceQuote key={record.feedback_id} record={record}/>)}</div><div className="card-actions"><Link className="button button-primary" to="/evidence/document-upload">View Supporting Evidence <Icon name="arrow"/></Link></div></Card>
  </>
}

function EvidenceQuote({ record }) {
  return <article className="quote-card"><div className="quote-meta"><span>{record.feedback_id}</span><Badge tone={record.sentiment === 'Negative' ? 'red' : 'neutral'}>{record.sentiment}</Badge><Badge tone={record.severity === 'High' ? 'orange' : 'neutral'}>{record.severity}</Badge></div><p>“{record.feedback_text}”</p><small>{record.channel} · {record.date}</small></article>
}

function SelectFilter({ label, value, onChange, options }) {
  return <label className="filter"><span>{label}</span><select value={value} onChange={(e) => onChange(e.target.value)}><option value="All">All</option>{options.map((option) => <option key={option}>{option}</option>)}</select></label>
}

function prioritizeDiverse(records) {
  const signature = (text) => text.toLowerCase()
    .replace(/^(honestly,\s*|please help\s*[—-]\s*|this is frustrating\.\s*)/, '')
    .replace(/[^a-z0-9 ]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
  const groups = new Map()
  records.forEach((record) => {
    const key = signature(record.feedback_text)
    groups.set(key, [...(groups.get(key) || []), record])
  })
  const ordered = []
  const queues = [...groups.values()]
  while (queues.some((queue) => queue.length)) {
    queues.forEach((queue) => { if (queue.length) ordered.push(queue.shift()) })
  }
  return ordered
}

function Evidence({ records }) {
  const docs = records.filter((r) => r.theme === 'Document Upload')
  const [severity, setSeverity] = useState('All'), [sentiment, setSentiment] = useState('All'), [channel, setChannel] = useState('All')
  const orderedDocs = prioritizeDiverse(docs)
  const filtered = orderedDocs.filter((r) => (severity === 'All' || r.severity === severity) && (sentiment === 'All' || r.sentiment === sentiment) && (channel === 'All' || r.channel === channel))
  const channels = [...new Set(docs.map((r) => r.channel))].sort()
  return <>
    <PageHeader backTo="/insights/document-upload" backLabel="Back to Document Upload Insight" title="Customer Evidence" subtitle="Original feedback supporting the Document Upload insight" />
    <div className="why-callout"><div className="callout-icon">i</div><div><strong>Why this matters</strong><p>AI-generated insights remain connected to the original customer feedback so Product Managers can verify the evidence before acting.</p></div></div>
    <div className="filters"><SelectFilter label="Severity" value={severity} onChange={setSeverity} options={SEVERITY_ORDER.filter((item) => docs.some((r) => r.severity === item))}/><SelectFilter label="Sentiment" value={sentiment} onChange={setSentiment} options={SENTIMENT_ORDER.filter((item) => docs.some((r) => r.sentiment === item))}/><SelectFilter label="Channel" value={channel} onChange={setChannel} options={channels}/><button className="clear-button" onClick={() => {setSeverity('All');setSentiment('All');setChannel('All')}}>Clear filters</button></div>
    <div className="evidence-status"><strong>{docs.length} Document Upload records</strong><span>Showing {filtered.length} of {docs.length} records</span></div>
    <Card className="table-card"><div className="evidence-table"><div className="table-head"><span>Feedback</span><span>Date</span><span>Channel</span><span>Journey Stage</span><span>Sentiment</span><span>Severity</span></div>{filtered.map((record) => <div className="table-row" key={record.feedback_id}><div><strong>{record.feedback_id}</strong><p>{record.feedback_text}</p></div><span>{new Date(`${record.date}T00:00:00`).toLocaleDateString('en-US',{month:'short',day:'numeric'})}</span><span>{record.channel}</span><span>{record.journey_stage}</span><span><Badge tone={record.sentiment === 'Negative' ? 'red' : 'neutral'}>{record.sentiment}</Badge></span><span><Badge tone={record.severity === 'High' ? 'orange' : 'neutral'}>{record.severity}</Badge></span></div>)}</div>{filtered.length === 0 && <div className="empty-state">No feedback records match these filters.</div>}</Card>
    <div className="page-actions"><Link className="button button-secondary" to="/insights/document-upload"><Icon name="back"/> Back to Insight</Link><Link className="button button-primary" to="/product-action/document-upload">Continue to Product Action <Icon name="arrow"/></Link></div>
  </>
}

function ProductAction() {
  const navigate = useNavigate()
  const [problem, setProblem] = useState('Customers submitting claim documents may lack clear confirmation that their upload was successfully received and recognized.')
  const [status, setStatus] = useState('Needs Investigation'), [notes, setNotes] = useState(''), [saved, setSaved] = useState(false)
  const save = () => { setSaved(true); window.setTimeout(() => setSaved(false), 3500) }
  return <>
    <PageHeader backTo="/evidence/document-upload" backLabel="Back to Evidence" eyebrow="Candidate Pain Point · Document Upload" title="Turn Insight into Action" subtitle="Structure an investigation. The Product Manager remains responsible for the decision." />
    <div className="action-grid">
      <div className="action-column">
        <Card className="suggestion-card"><div className="suggestion-label"><Badge tone="blue">AI-assisted</Badge><span>Suggested starting point</span></div><h2>AI-Assisted Problem Statement</h2><blockquote>“Customers may lack confidence that uploaded documents were received or recognized.”</blockquote><p>This is a synthesis of feedback—not a proven root cause.</p></Card>
        <Card><SectionTitle title="PM Problem Statement" subtitle="Review and edit the framing in your own words"/><label className="field"><span>Problem statement</span><textarea rows="5" value={problem} onChange={(e) => setProblem(e.target.value)}/><small>{problem.length} characters · Editable by the Product Manager</small></label></Card>
      </div>
      <div className="action-column">
        <Card><SectionTitle title="Questions to Investigate" subtitle="Questions to guide further investigation"/><ul className="question-list"><li>Is upload confirmation clear enough?</li><li>Why are some users asked for documents again after uploading?</li><li>Are missing-document messages related to upload recognition or document requirements?</li></ul></Card>
        <Card><div className="form-grid"><label className="field"><span>Decision Status</span><select value={status} onChange={(e) => setStatus(e.target.value)}><option>Needs Investigation</option><option>Monitor</option><option>Discuss with Team</option><option>Insufficient Evidence</option></select></label><label className="field"><span>PM Notes <em>Optional</em></span><textarea rows="4" placeholder="Add context, assumptions, or follow-up notes…" value={notes} onChange={(e) => setNotes(e.target.value)}/></label></div></Card>
      </div>
    </div>
    <div className="decision-footer"><p>Capture the PM’s framing, decision status, and notes for this prototype.</p><div><button className="button button-secondary" onClick={() => navigate('/evidence/document-upload')}>Back to Evidence</button><button className="button button-primary" onClick={save}>Save Product Insight</button></div></div>
    {saved && <div className="toast" role="status"><span><Icon name="check"/></span><div><strong>Product insight saved</strong><p>Saved for prototype demo.</p></div></div>}
  </>
}

function App() {
  const { records, error } = useFeedback()
  return <Layout>{records.length === 0 ? <LoadingState error={error}/> : <Routes><Route path="/" element={<Overview records={records}/>}/><Route path="/overview" element={<Overview records={records}/>}/><Route path="/insights/document-upload" element={<Insight records={records}/>}/><Route path="/evidence/document-upload" element={<Evidence records={records}/>}/><Route path="/product-action/document-upload" element={<ProductAction/>}/><Route path="*" element={<Overview records={records}/>}/></Routes>}</Layout>
}

export default App
