var sidenavElem = document.querySelector('.sidenav');
var sidenavInstance = M.Sidenav.init(sidenavElem, {'edge' : 'left'});

// JS for user creation modal
var createUserElem = document.querySelector('.createuser-modal');
var createUserModal = M.Modal.init(createUserElem);
var createUserModalPriviledgesSelect = document.querySelector('#diritti');
var createUserModalPriviledgesSelector = M.FormSelect.init(createUserModalPriviledgesSelect);

// JS for managing groups modal
var manageGroupsElem = document.querySelector('.managegroups-modal');
var manageGroupsModal = M.Modal.init(manageGroupsElem);
var manageGroupsModalNewTypeSelect = document.querySelector('#creategroup-type');
var manageGroupsModalNewTypeSelector = M.FormSelect.init(manageGroupsModalNewTypeSelect);
var manageGroupsModalDelTypeSelect = document.querySelector('#deletegroup-type');
var manageGroupsModalDelTypeSelector = M.FormSelect.init(manageGroupsModalDelTypeSelect);

// JS for CSV upload modal
var uploadCSVElem = document.querySelector('.uploadcsv-modal');
var uploadCSVModal = M.Modal.init(uploadCSVElem);
