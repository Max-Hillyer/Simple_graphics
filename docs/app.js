const eventExamples = {
  tick: { code: '<span class="code-purple">@on_tick</span>\n<span class="code-blue">def</span> update():\n    ball.x += velocity\n    ball.y += gravity', caption: 'The default callback runs once every frame.' },
  press: { code: '<span class="code-purple">@on_press</span>(<span class="code-yellow">"space"</span>)\n<span class="code-blue">def</span> launch():\n    ball.visible = <span class="code-yellow">True</span>', caption: 'Listen for one key, or omit the key to hear any press.' },
  hold: { code: '<span class="code-purple">@on_hold</span>(<span class="code-yellow">"left,right"</span>)\n<span class="code-blue">def</span> steer(key):\n    paddle.x += direction(key)', caption: 'Hold a key to run movement continuously.' },
  click: { code: '<span class="code-purple">@on_click</span>(button)\n<span class="code-blue">def</span> clicked():\n    game.score += <span class="code-yellow">1</span>', caption: 'Target a shape, or listen for clicks anywhere.' },
  hover: { code: '<span class="code-purple">@on_hover</span>(planet)\n<span class="code-blue">def</span> inspect():\n    label.visible = <span class="code-yellow">True</span>', caption: 'Run while the pointer is over a particular shape.' },
  drag: { code: '<span class="code-purple">@on_drag</span>(triangle)\n<span class="code-blue">def</span> move():\n    label.text = <span class="code-yellow">"moving"</span>', caption: 'Pair with draggable=True for direct manipulation.' }
};

const eventCode = document.querySelector('#event-code code');
const eventCaption = document.querySelector('#event-caption');
document.querySelectorAll('.event-tab').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelector('.event-tab.is-active')?.classList.remove('is-active');
    tab.classList.add('is-active');
    const example = eventExamples[tab.dataset.event];
    eventCode.innerHTML = example.code;
    eventCaption.textContent = example.caption;
  });
});

document.querySelector('.copy-button')?.addEventListener('click', async (event) => {
  const button = event.currentTarget;
  const text = document.querySelector(`#${button.dataset.copy}`).innerText;
  await navigator.clipboard.writeText(text);
  button.textContent = 'Copied';
  setTimeout(() => { button.textContent = 'Copy code'; }, 1400);
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
