const quiz = document.getElementById('quiz');
const container = document.getElementById('questions');
const result = document.getElementById('result');
let questions = [];
async function loadQuestions() {
  try {
    const response = await fetch('/api/questions');
    if (!response.ok) throw new Error('Unable to load questions');
    questions = await response.json();
    container.replaceChildren();
    for (const q of questions) {
      const fieldset = document.createElement('fieldset');
      fieldset.className = 'question';
      const legend = document.createElement('legend');
      legend.textContent = `${q.id}. ${q.question}`;
      fieldset.append(legend);
      q.options.forEach((option, index) => {
        const label = document.createElement('label');
        label.className = 'option';
        const input = document.createElement('input');
        input.type = 'radio'; input.name = `q${q.id}`; input.value = index;
        label.append(input, document.createTextNode(option));
        fieldset.append(label);
      });
      container.append(fieldset);
    }
  } catch (error) { container.textContent = error.message; }
}
quiz.addEventListener('submit', async event => {
  event.preventDefault();
  if (!questions.length) return;
  const answers = {};
  for (const q of questions) {
    const selected = quiz.querySelector(`input[name="q${q.id}"]:checked`);
    if (!selected) { result.textContent = 'Please answer all questions first.'; return; }
    answers[q.id] = Number(selected.value);
  }
  try {
    const response = await fetch('/api/grade', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({answers})});
    if (!response.ok) throw new Error('Could not grade answers');
    const data = await response.json();
    result.textContent = `You scored ${data.score} out of ${data.total}!`;
  } catch (error) { result.textContent = error.message; }
});
loadQuestions();
