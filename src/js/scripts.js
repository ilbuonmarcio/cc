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
var manageGroupsModalNewTypeSelect = document.querySelector('#creategroup-select');
var manageGroupsModalNewTypeSelector = M.FormSelect.init(manageGroupsModalNewTypeSelect);
var manageGroupsModalDelTypeSelect = document.querySelector('#deletegroup-select');
var manageGroupsModalDelTypeSelector = M.FormSelect.init(manageGroupsModalDelTypeSelect);

// JS for CSV upload modal
var uploadCSVElem = document.querySelector('.uploadcsv-modal');
var uploadCSVModal = M.Modal.init(uploadCSVElem);
var uploadCSVModalSelect = document.querySelector('#uploadcsv-select');
var uploadCSVModalSelector = M.FormSelect.init(uploadCSVModalSelect);

// JS for configuring cc parameters modal
var configCCElem = document.querySelector('.configcc-modal');
var configCCModal = M.Modal.init(configCCElem);

// JS for generate cc modal
var genCCElem = document.querySelector('.gencc-modal');
var genCCModal = M.Modal.init(genCCElem);
