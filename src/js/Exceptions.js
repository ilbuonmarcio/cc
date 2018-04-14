class InvalidUsernameOrPasswordLengthException extends Error{
  constructor(msg){
    super(msg);
    this.name = 'InvalidUsernameOrPasswordLengthException';
  }
}

class GroupNameTooSmallException extends Error{
  constructor(msg){
    super(msg);
    this.name = 'GroupNameTooSmallException';
  }
}

class FilePathTooSmallException extends Error{
  constructor(msg){
    super(msg);
    this.name = 'FilePathTooSmallException';
  }
}

class EmptyFieldsOnConfigureCCPanelUpload extends Error{
  constructor(msg){
    super(msg);
    this.name = 'EmptyFieldsOnConfigureCCPanelUpload';
  }
}
