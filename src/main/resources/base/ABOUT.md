This directory can be used to store assets needed by the application.

#### Note 

You must use `ApplicationContext.get_resource(<relativePath>)`. 
This means we will need to use some sort of dependency injection to have access to the `ApplicationContext` singleton wherever we need to access resources.