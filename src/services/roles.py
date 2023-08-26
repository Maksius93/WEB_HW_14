from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and takes in any arguments that are required to do so.
        In this case, we're taking in a list of allowed roles.

        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles for a user
        :return: The self object
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two parameters: request and user. The request parameter is the Request object, which contains all of
        the information about the incoming HTTP request (headers, body, etc.). The second parameter depends on whether or not
        you have defined a dependency for your route. In this case we are using Depends(auth_service.get_current_user) as our
        dependency so it will call auth_service's get current user function and pass in whatever it returns as our second argument.

        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param user: User: Get the user object from the auth_service
        :return: A function that takes a request and user as parameters
        :doc-author: Trelent
        """
        print(user.role)
        print(self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")