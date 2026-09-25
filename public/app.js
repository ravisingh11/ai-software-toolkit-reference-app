'use strict';

const $ = (selector) => document.querySelector(selector);
const state = { session: null, issues: [], status: 'all', selected: null, detailRequest: 0, createRequest: 0 };
const statusLabels = { triage: 'Triage', in_progress: 'In progress', done: 'Done' };
const transitions = { triage: ['triage', 'in_progress'], in_progress: ['in_progress', 'triage', 'done'], done: ['done', 'in_progress'] };

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function notify(message, error = false) {
  const node = $('#notification');
  node.textContent = message;
  node.classList.toggle('error', error);
  node.hidden = !message;
}

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: options.body ? { 'Content-Type': 'application/json' } : {},
  });
  let data;
  try {
    data = await response.json();
  } catch {
    if (response.ok) throw new Error('The server returned an unreadable response. The action may have completed; check the board before trying again.');
    data = {};
  }
  if (!response.ok) {
    if (response.status === 401) {
      state.session = null;
      state.issues = [];
      state.selected = null;
      state.detailRequest += 1;
      document.querySelectorAll('dialog[open]').forEach((dialog) => dialog.close());
      updateSession();
      renderIssues();
    }
    const error = new Error(data.error || 'Something went wrong. Please try again.');
    error.status = response.status;
    throw error;
  }
  return data;
}

async function busy(button, label, task) {
  const original = button.textContent;
  button.disabled = true;
  button.textContent = label;
  try { await task(); } finally {
    button.textContent = original;
    button.disabled = false;
    updateSession();
  }
}

function updateSession() {
  const session = state.session;
  const editor = session?.role === 'editor';
  $('#new-issue').disabled = !editor;
  $('#role-note').hidden = !session || editor;
  $('#start-session').textContent = session ? 'Start fresh ↗' : 'Start demo ↗';
  $('#session-description').textContent = session
    ? `Your isolated ${session.role} board is ready. Starting fresh replaces this browser’s current board.`
    : 'An isolated board. A fresh place to experiment.';
  $('#status-submit').disabled = !editor;
  $('#issue-status').disabled = !editor;
  $('#comment-body').disabled = !editor;
  $('#comment-submit').disabled = !editor;
  $('#create-submit').disabled = !editor;
}

function emptyState(title, description) {
  const node = element('div', 'empty-state');
  node.append(element('span', 'empty-icon', '↗'), element('h3', '', title), element('p', '', description));
  return node;
}

function renderIssues() {
  const query = $('#search').value.trim().toLowerCase();
  const priority = $('#priority-filter').value;
  const filtered = state.issues.filter((issue) =>
    (state.status === 'all' || issue.status === state.status)
    && (priority === 'all' || issue.priority === priority)
    && `${issue.title} ${issue.description}`.toLowerCase().includes(query));
  $('#issue-count').textContent = String(state.issues.length);
  document.querySelectorAll('[data-count]').forEach((node) => {
    node.textContent = String(state.issues.filter((issue) => node.dataset.count === 'all' || issue.status === node.dataset.count).length);
  });
  const list = $('#issue-list');
  list.replaceChildren();
  if (!state.session) {
    list.append(emptyState('A blank page, full of possibility.', 'Start a demo above to explore your own seeded issue board.'));
  } else if (!filtered.length) {
    list.append(emptyState('A little breathing room.', 'No issues match this view. Try another filter or create a new issue.'));
  } else {
    filtered.forEach((issue) => {
      const card = element('button', 'issue-card');
      card.type = 'button';
      card.dataset.issueId = issue.id;
      card.setAttribute('aria-label', `Open issue: ${issue.title}`);
      const main = element('span', 'issue-main');
      main.append(element('span', 'issue-title', issue.title), element('span', 'issue-preview', issue.description || 'A fresh note, ready for more detail.'));
      card.append(element('span', 'issue-reference', `FN–${String(issue.id).slice(0, 6).toUpperCase()}`), main,
        element('span', `priority priority-${issue.priority}`, issue.priority),
        element('span', `status status-${issue.status}`, statusLabels[issue.status]), element('span', 'issue-arrow', '↗'));
      card.addEventListener('click', () => openIssue(issue));
      list.append(card);
    });
  }
  $('#board-summary').textContent = state.session
    ? `${filtered.length} of ${state.issues.length} issues · Your changes stay in your own demo workspace.`
    : 'Your changes stay in your own demo workspace.';
}

async function loadIssues() {
  const data = await api('/issues');
  state.issues = data.issues;
  renderIssues();
}

function renderDetail() {
  const issue = state.selected;
  if (!issue) return;
  $('#detail-title').textContent = issue.title;
  $('#detail-reference').textContent = `FIELDNOTE / ${String(issue.id).slice(0, 8).toUpperCase()}`;
  $('#detail-description').textContent = issue.description || 'No description yet.';
  $('#detail-meta').replaceChildren(element('span', `priority priority-${issue.priority}`, issue.priority), element('span', `status status-${issue.status}`, statusLabels[issue.status]));
  $('#issue-status').replaceChildren(...transitions[issue.status].map((status) => {
    const option = element('option', '', statusLabels[status]);
    option.value = status;
    return option;
  }));
  updateSession();
}

async function openIssue(issue) {
  state.selected = issue;
  const request = ++state.detailRequest;
  $('#detail-error').textContent = '';
  $('#comment-form').reset();
  renderDetail();
  $('#comment-list').replaceChildren(element('p', 'comment-empty', 'Loading the conversation…'));
  $('#detail-dialog').showModal();
  try {
    const { comments } = await api(`/issues/${encodeURIComponent(issue.id)}/comments`);
    if (request === state.detailRequest) renderComments(comments);
  } catch (error) {
    if (request === state.detailRequest) $('#detail-error').textContent = error.message;
  }
}

function renderComments(comments) {
  const list = $('#comment-list');
  list.replaceChildren();
  if (!comments.length) list.append(element('p', 'comment-empty', 'No comments yet. Every conversation starts somewhere.'));
  comments.forEach((comment) => {
    const node = element('article', 'comment');
    const date = new Date(comment.createdAt);
    const time = element('time', '', Number.isNaN(date.valueOf()) ? 'Just now' : date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }));
    if (!Number.isNaN(date.valueOf())) time.dateTime = date.toISOString();
    node.append(time, element('p', '', comment.body));
    list.append(node);
  });
}

$('#start-session').addEventListener('click', async () => {
  notify('');
  await busy($('#start-session'), 'Preparing…', async () => {
    try {
      state.session = await api('/session', { method: 'POST', body: JSON.stringify({ role: $('#demo-role').value }) });
      state.selected = null;
      state.detailRequest += 1;
      state.issues = [];
      state.status = 'all';
      $('#search').value = '';
      $('#priority-filter').value = 'all';
      document.querySelectorAll('[data-status]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.status === 'all')));
      updateSession();
      await loadIssues();
      notify(`Your fresh ${state.session.role} demo is ready. This board expires after 24 hours.`);
    } catch (error) { renderIssues(); notify(error.message, true); }
  });
});

$('#new-issue').addEventListener('click', () => {
  $('#create-form').reset();
  $('#create-error').textContent = '';
  $('#create-dialog').showModal();
  $('#issue-title').focus();
});
document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => document.getElementById(button.dataset.close).close()));
$('#detail-dialog').addEventListener('close', () => { state.detailRequest += 1; });
$('#create-dialog').addEventListener('close', () => { state.createRequest += 1; });
document.querySelectorAll('[data-status]').forEach((button) => button.addEventListener('click', () => {
  state.status = button.dataset.status;
  document.querySelectorAll('[data-status]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  renderIssues();
}));
$('#search').addEventListener('input', renderIssues);
$('#priority-filter').addEventListener('change', renderIssues);

$('#create-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  $('#create-error').textContent = '';
  const session = state.session;
  const request = state.createRequest;
  await busy($('#create-submit'), 'Creating…', async () => {
    try {
      const { issue } = await api('/issues', { method: 'POST', body: JSON.stringify({ title: $('#issue-title').value.trim(), description: $('#issue-description').value.trim(), priority: $('#issue-priority').value }) });
      if (session !== state.session) return;
      state.issues.unshift(issue);
      renderIssues();
      if (request === state.createRequest) $('#create-dialog').close();
      notify('Issue created. You’ll find it in Triage.');
    } catch (error) {
      if (session === state.session && request === state.createRequest) $('#create-error').textContent = error.message;
    }
  });
});

$('#status-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!state.selected) return;
  $('#detail-error').textContent = '';
  const issueId = state.selected.id;
  const request = state.detailRequest;
  const session = state.session;
  await busy($('#status-submit'), 'Updating…', async () => {
    try {
      const { issue } = await api(`/issues/${encodeURIComponent(issueId)}`, { method: 'PATCH', body: JSON.stringify({ status: $('#issue-status').value }) });
      if (session !== state.session) return;
      state.issues = state.issues.map((item) => item.id === issue.id ? issue : item);
      renderIssues();
      if (request === state.detailRequest && state.selected?.id === issueId) {
        state.selected = issue;
        renderDetail();
        notify(`Issue moved to ${statusLabels[issue.status]}.`);
      }
    } catch (error) {
      if (session === state.session && request === state.detailRequest && state.selected?.id === issueId) $('#detail-error').textContent = error.message;
    }
  });
});

$('#comment-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!state.selected) return;
  $('#detail-error').textContent = '';
  const issueId = state.selected.id;
  const request = state.detailRequest;
  await busy($('#comment-submit'), 'Adding…', async () => {
    try {
      await api(`/issues/${encodeURIComponent(issueId)}/comments`, { method: 'POST', body: JSON.stringify({ body: $('#comment-body').value.trim() }) });
      // Clear after a confirmed write so a failed refresh cannot duplicate the comment.
      if (request === state.detailRequest) $('#comment-form').reset();
      const { comments } = await api(`/issues/${encodeURIComponent(issueId)}/comments`);
      if (request === state.detailRequest) renderComments(comments);
    } catch (error) {
      if (request === state.detailRequest) $('#detail-error').textContent = error.message;
    }
  });
});

async function restoreSession() {
  $('#start-session').disabled = true;
  try {
    state.session = await api('/session');
    $('#demo-role').value = state.session.role;
    updateSession();
    await loadIssues();
  } catch (error) {
    if (error.status !== 401) notify(`Could not restore your board. ${error.message}`, true);
  } finally { $('#start-session').disabled = false; updateSession(); }
}
restoreSession();
