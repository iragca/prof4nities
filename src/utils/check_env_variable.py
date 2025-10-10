def check_env_variable(var, var_name: str, important: bool = False):
    """Check if an environment variable is set."""
    if var is None:
        if important:
            raise EnvironmentError(f"Environment variable '{var_name}' is not set.")
        else:
            print(f"Environment variable {var_name} is not set.")
        return None
    return var
