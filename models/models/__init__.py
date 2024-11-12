#!/usr/bin/python3
"""This module contains the constructor"""
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            *args (tuple): Unused positional arguments.
            **kwargs (dict): Keyword arguments used to initialize the object.
        """
        if (kwargs is not None):
            for key,value in kwargs.iteritems():
                if key != __class__:
                    setattr(self,key,value)
                if "create_at" in kwargs:
                    self.create_at = datetime.fromisoformat(kwargs["create_at"])
                if "update_at" in kwargs:
                    self.update_at = datetime.fromisoformat(kwargs["update_at"])
        else:
            