var sidenavElem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(sidenavElem, {'edge' : 'left'});

// JS for user creation modal
var createUserElem = document.querySelector('.createuser-modal');
var createUserModal = M.Modal.init(createUserElem);
var createUserModalSelect = document.querySelector('#diritti');
var createUserModalPriviledgesSelector = M.FormSelect.init(createUserModalSelect);

// JS for managing groups modal
var manageGroupsElem = document.querySelector('.managegroups-modal');
var manageGroupsModal = M.Modal.init(manageGroupsElem);
var manageGroupsModalSelect = document.querySelector('#managegroups-modal-list-group-selector');
var manageGroupsModalSelector = M.FormSelect.init(manageGroupsModalSelect);

// JS for CSV upload modal
var uploadCSVElem = document.querySelector('.uploadcsv-modal');
var uploadCSVModal = M.Modal.init(uploadCSVElem);
