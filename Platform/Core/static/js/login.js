(function () {
  var form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', function (event) {
    var username = document.getElementById('id_username');
    var password = document.getElementById('id_password');

    if (!username || !password) return;

    var user = username.value.trim();
    var pass = password.value.trim();

    if (!user || !pass) {
      event.preventDefault();
      alert('Preencha usuario e senha.');
      return;
    }

    var button = form.querySelector('button[type="submit"]');
    if (button) {
      button.disabled = true;
      button.textContent = 'Entrando...';
    }
  });
})();
