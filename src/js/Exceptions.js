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
