var sidenavElem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(sidenavElem, {'edge' : 'left'});

// JS for user creation modal
var createUserElem = document.querySelector('.createuser-modal');
var createUserModal = M.Modal.init(createUserElem);
var createUserModalSelect = document.querySelector('select');
var createUserModelPriviledgesSelector = M.FormSelect.init(createUserModalSelect);

// JS for CSV upload modal
var uploadCSVElem = document.querySelector('.uploadcsv-modal');
var uploadCSVModal = M.Modal.init(uploadCSVElem);
