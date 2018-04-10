class InvalidUsernameOrPasswordLengthException extends Error{
  constructor(msg){
    super(msg);
    this.name = 'InvalidUsernameOrPasswordLengthException';
  }
}
