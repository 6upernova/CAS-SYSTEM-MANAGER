(function() {
  "use strict";

    // code to handle user registration
    document.addEventListener('DOMContentLoaded', function() {
      const form = document.querySelector('form');
      const nameField = document.getElementById('name')
      const nameError = document.getElementById('nameError');
      const userField = document.getElementById('username');
      const userError = document.getElementById('usernameError');
      const emailField = document.getElementById('email');
      const passwordField = document.getElementById('password');
      const emailError = document.getElementById('emailError');
      const passwordError = document.getElementById('passwordError');
      const submitBtn = document.getElementById('submitBtn');
      let emailExistTimeout;

      form.addEventListener('submit', function(event) {
        if (!validateForm()) {
          event.preventDefault(); // prevent submitting the form
        }
      });

      emailField.addEventListener('input', function() {
        clearTimeout(emailExistTimeout);
        const email = emailField.value.trim();

        if (email === '') {
          emailField.classList.remove('is-invalid');
          emailError.textContent = '';
          submitBtn.disabled = false; // enable submit button
        } else {
          emailExistTimeout = setTimeout(function() {
            axios.post('/check_email', { email })
              .then(function(response) {
                if (response.data.exists) {
                  emailField.classList.add('is-invalid');
                  emailError.textContent = 'Email already exists!';
                  submitBtn.disabled = true; // disable submit button
                } else {
                  emailField.classList.remove('is-invalid');
                  emailError.textContent = '';
                  submitBtn.disabled = false; // enable submit button
                }
              })
              .catch(function(error) {
                console.error(error);
              });
          }, 250);
        }
      });

      function ValidateEmail(email) {
        // regular expression to validate emails
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      }

      function validateForm() {
        let isValid = true;

        if (nameField.value.trim() === '') {
          nameField.classList.add('is-invalid');
          nameError.textContent = 'Please enter a valid name!';
          isValid = false;
        } else {
          nameField.classList.remove('is-invalid');
          nameError.textContent = '';
        }

        if (userField.value.trim() === '') {
          userField.classList.add('is-invalid');
          userError.textContent = 'Please enter a valid username!';
          isValid = false;
        } else {
          userField.classList.remove('is-invalid');
          userError.textContent = '';
        }

        if (emailField.value.trim() === '') {
          emailField.classList.add('is-invalid');
          emailError.textContent = 'Please enter a valid Email address!';
          isValid = false;
        } else if (!ValidateEmail(emailField.value)) {
          emailField.classList.add('is-invalid');
          emailError.textContent = 'Please enter a valid Email address!';
          isValid = false;
        } else if (emailField.classList.contains('is-invalid')) {
          isValid = false;
        } else {
          emailField.classList.remove('is-invalid');
          emailError.textContent = '';
        }

        if (passwordField.value.trim() === '') {
          passwordField.classList.add('is-invalid');
          passwordError.textContent = 'Please enter your password!';
          isValid = false;
        } else {
          passwordField.classList.remove('is-invalid');
          passwordError.textContent = '';
        }

        return isValid;
      }
    });


  document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const confirmationField = document.getElementById('confirmation');
    const confirmationError = document.getElementById('confirmationError');
    const submitBtn = document.getElementById('submitBtn');

    function validatePasswords() {
      if (passwordField.value !== confirmationField.value) {
        confirmationField.classList.add('is-invalid');
        confirmationError.textContent = 'Passwords must match!';
        submitBtn.disabled = true; // disable submit button
      } else {
        confirmationField.classList.remove('is-invalid');
        confirmationError.textContent = '';
        submitBtn.disabled = false; // enable submit button
      }
    }

    passwordField.addEventListener('input', validatePasswords);
    confirmationField.addEventListener('input', validatePasswords);
  });

  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener));
    } else {
      select(el, all).addEventListener(type, listener);
    }
  };

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener);
  };

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar');
    });
  }


// Get all plan edit buttons
var editPlanBtns = document.querySelectorAll('.edit-plan-btn');

// Handle click event for each button
editPlanBtns.forEach(function(editPlanBtn) {
  editPlanBtn.addEventListener('click', function() {
    var planId = this.getAttribute('data-plan-id');

    // Make an AJAX request to get the data
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_plan/' + planId);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var plan = JSON.parse(xhr.responseText);

        // Complete modal with the data
        document.getElementById('editPlanName').value = plan.name;
        document.getElementById('editPlanPrice').value = plan.price;
        document.getElementById('editDays').value = plan.days;
        document.getElementById('editPlanDescription').value = plan.description;

        // Get form reference
        var form = document.getElementById('editPlanForm');

        // Update the 'action' attribute of the form
        form.action = '/edit_plan/' + planId;

        // Open edit plan modal
        var editPlanModal = new bootstrap.Modal(document.getElementById('editPlanModal'));
        editPlanModal.show();

        var closeButtons = document.querySelectorAll('[data-bs-dismiss="modal"]');
        closeButtons.forEach(function(closeButton) {
          closeButton.addEventListener('click', function() {
            editPlanModal.hide();
          });
        });

      } else {
        alert('Error al obtener los datos del plan');
      }

    };
    xhr.send();
  });
});



// Get all member buttons
var editMemberBtns = document.querySelectorAll('.edit-member-btn');

// Handle click event for each button
editMemberBtns.forEach(function(editMemberBtn) {
  editMemberBtn.addEventListener('click', function() {
    var memberId = this.getAttribute('data-member-id');

    // Make an AJAX request to get the data
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_member/' + memberId);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var member = JSON.parse(xhr.responseText);

        // Complete modal with the data
        document.getElementById('editMembershipName').value = member.name;
        console.log('Plan ID:', member.plan_id);
        console.log('Routine ID:', member.routine_id);

        // Select the correct plan
        var planSelect = document.getElementById('editMembershipPlan');
        for (var i = 0; i < planSelect.options.length; i++) {
          if (planSelect.options[i].value == member.plan_id) {
            planSelect.options[i].selected = true;
            break;
          }
        }

        // Select the correct routine
        var routineSelect = document.getElementById('editMembershipRoutine');
        for (var j = 0; j < routineSelect.options.length; j++) {
          if (routineSelect.options[j].value == member.routine_id) {
            routineSelect.options[j].selected = true;
            break;
          }
        }

        document.getElementById('editMembershipEmail').value = member.email;
        document.getElementById('editMembershipNumber').value = member.number;
        document.getElementById('editMembershipDescription').value = member.description;
       
        // Get form reference
        var form = document.getElementById('editMemberForm');

        // Update the 'action' attribute of the form
        form.action = '/edit_member/' + memberId;

        // Open edit member modal
        var editMemberModal = new bootstrap.Modal(document.getElementById('editMembershipModal'));
        editMemberModal.show();

        var closeButtons = document.querySelectorAll('[data-bs-dismiss="modal"]');
        closeButtons.forEach(function(closeButton) {
          closeButton.addEventListener('click', function() {
            editMemberModal.hide();
          });
        });

      } else {
        alert('Error al obtener los datos del miembro');
      }

    };
    xhr.send();
  });
});

  var spanishI18n = {
    previousMonth: 'Mes anterior',
    nextMonth: 'Mes siguiente',
    months: [
      'Enero',
      'Febrero',
      'Marzo',
      'Abril',
      'Mayo',
      'Junio',
      'Julio',
      'Agosto',
      'Septiembre',
      'Octubre',
      'Noviembre',
      'Diciembre'
    ],
    weekdays: [
      'Domingo',
      'Lunes',
      'Martes',
      'Miércoles',
      'Jueves',
      'Viernes',
      'Sábado'
    ],
    weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
  };

  var picker = new Pikaday({
    field: document.getElementById('datepicker'),
    format: 'DD/MM/YYYY',
    minDate: new Date(),
    defaultDate: new Date(),
    i18n: spanishI18n,
    toString(date, format) {
      // Usa el formato especificado al configurar el datepicker
      return moment(date).format(format);
    }
  });
  

  





  var currentDate = moment().format('DD/MM/YYYY'); // Get formated current date
  console.log(currentDate);
  document.getElementById('datepicker').setAttribute('placeholder', currentDate);

})();

(function() {
  $(document).ready(function() {
    $('#toggleForm').submit(function(e) {
      e.preventDefault();

      $.post($(this).attr('action'), function(data) {
        // Assuming data is a JSON response from the server
        if (data.reminded == 2) {
          $('#toggleForm button').removeClass('btn-info').addClass('btn-outline-info');
        } else {
          $('#toggleForm button').removeClass('btn-outline-info').addClass('btn-info');
        }
      })
      .fail(function() {
        console.error("Error in AJAX request");
      });
    });
  });
})();

// prevents user to click in a pdf button that doesnt have a pdf
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    var openPdfButton = document.getElementById('openPdfButton');
    
    openPdfButton.addEventListener('click', function(event) {
        if (openPdfButton.hasAttribute('disabled')) {
            event.preventDefault(); // Evitar que se ejecute el evento de clic
            alert('No se ha cargado ningún archivo PDF.');
        }
    });

    // Deshabilitar el clic derecho en el botón para prevenir menú contextual
    openPdfButton.addEventListener('contextmenu', function(event) {
        event.preventDefault();
    });
});

})();



(function(){
  
  document.addEventListener("DOMContentLoaded", function () {
    // Obtén todas las filas de la tabla
    var rows = document.querySelectorAll("#eventsTable tbody tr");

    // Para cada fila, agrega un listener de clic
    rows.forEach(function (row) {
      row.addEventListener("click", function () {
        // Obtiene el ID de la fila
        if (event.target.tagName.toLowerCase() !== 'button') {
          var rowId = row.getAttribute("data-row-id");

          // Redirige a la página del evento con el ID
          window.location.href = "/event/" + rowId;
        }
      });
    });
  });

})();

(function(){
  // Funcion para poder editar las celdas
  document.querySelectorAll('#editableTable{{ loop.index }} [contenteditable="true"]').forEach(function (cell) {
    cell.addEventListener('input', function () {
        var newText = this.innerText;
        var rowId = this.closest('tr').dataset.rowId;
        var tableId = this.closest('table').id;

        saveData(tableId, rowId, this.cellIndex, newText);
    });
});

function saveData(tableId, rowId, columnIndex, newText) {
  // Funcion para guardar los datos individualmente de cada celda
    fetch('/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            tableId: tableId,
            rowId: rowId,
            columnIndex: columnIndex,
            newText: newText,
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Datos guardados con éxito:', data);
        })
        .catch(error => {
            console.error('Error al guardar los datos:', error);
        });
}

})();