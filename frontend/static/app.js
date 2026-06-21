const API_BASE = (function(){
  // point to backend API; update if backend runs on different host/port
  return 'http://127.0.0.1:8000/api';
})();

function qs(sel){return document.querySelector(sel)}
function qsa(sel){return Array.from(document.querySelectorAll(sel))}

function showPage(id){
  qsa('.page').forEach(p=>p.classList.add('hidden'));
  qs('#page-'+id).classList.remove('hidden');
}

// Navigation
qs('#nav-login').addEventListener('click', ()=>showPage('login'));
qs('#nav-dashboard').addEventListener('click', ()=>showPage('dashboard'));
qs('#nav-employees').addEventListener('click', ()=>showPage('employees'));
qs('#nav-predict').addEventListener('click', ()=>showPage('predict'));

qs('#api-base').textContent = API_BASE;

// Login
qs('#login-form').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const username = qs('#login-username').value;
  const password = qs('#login-password').value;
  const payload = {username, email: username+'@example.com', password};
  try{
    const res = await fetch(API_BASE+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(!res.ok) throw new Error('Login failed');
    const data = await res.json();
    localStorage.setItem('access_token', data.access_token);
    qs('#login-message').textContent = 'Logged in';
    showPage('dashboard');
    loadDashboard();
  }catch(err){
    qs('#login-message').textContent = err.message;
  }
});

// Employees
async function loadEmployees(){
  const token = localStorage.getItem('access_token');
  const res = await fetch(API_BASE+'/employees', {headers: token?{Authorization:'Bearer '+token}:{}});
  if(!res.ok){
    qs('#employees-list').innerHTML = '<li>Failed to load</li>';
    return;
  }
  const list = await res.json();
  qs('#employees-list').innerHTML = list.map(e=>`<li>${e.employee_code} — ${e.first_name} ${e.last_name||''}</li>`).join('')
}

qs('#refresh-employees').addEventListener('click', loadEmployees);

// Predict
qs('#predict-form').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const body = {
    employee_id: Number(qs('#p-employee-id').value),
    working_hours_per_day: Number(qs('#p-working-hours').value),
    overtime_hours: Number(qs('#p-overtime').value),
    meeting_hours: Number(qs('#p-meetings').value),
    leave_count: Number(qs('#p-leave-count').value),
    late_arrivals: Number(qs('#p-late').value),
    task_completion_percent: Number(qs('#p-task-complete').value),
    performance_rating: Number(qs('#p-rating').value)
  };
  try{
    const res = await fetch(API_BASE+'/predict/burnout', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    const data = await res.json();
    qs('#predict-result').textContent = JSON.stringify(data);
  }catch(err){
    qs('#predict-result').textContent = 'Error: '+err.message;
  }
});

// Dashboard
async function loadDashboard(){
  qs('#dashboard-content').textContent = 'Loading...';
  // show simple counts
  try{
    const res = await fetch(API_BASE+'/employees');
    if(!res.ok) throw new Error('Failed');
    const list = await res.json();
    qs('#dashboard-content').innerHTML = `<p>Total employees: ${list.length}</p>`;
  }catch(err){
    qs('#dashboard-content').textContent = 'Unable to load dashboard';
  }
}

// Init
showPage('login');
