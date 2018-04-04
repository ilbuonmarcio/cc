var elem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(elem, {'edge' : 'left'});

var elem = document.querySelector('.modal');
var createUserModal = M.Modal.init(elem);

var elem = document.querySelector('select');
var createUserModelPriviledgesSelector = M.FormSelect.init(elem);
