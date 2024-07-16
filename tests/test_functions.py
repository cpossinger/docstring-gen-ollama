class BankAccount:
    """
    Represents a bank account with deposit and withdrawal functionality.

    Attributes:
        name (str): The name of the account holder.
        balance (int): The initial balance of the account, defaulting to 0 if not specified.

    Methods:
        __init__(name, balance=0): Initializes the bank account with the given name and optional initial balance.
        deposit(amount): Deposits the given amount into the account, returning the new balance.
        withdraw(amount): Withdraws the given amount from the account, returning the new balance if sufficient funds are available. If not, prints an error message and does not update the balance.

    Raises:
        ValueError: Not raised by this class, but may be raised by underlying logic (e.g., attempting to withdraw more than the initial balance).
    """

    def __init__(self, name, balance=0):
        """Initializes a new bank account with a given name and optional initial balance.

        Args:
            self: The instance of the BankAccount class.
            name (str): The name to be associated with this bank account.
            balance (int, optional): The initial balance. Defaults to 0.
        """
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits a given amount into the account.

        Args:
            self (object): The current state of the object.
            amount (float): The amount to be deposited.

        Returns:
            float: The updated balance after depositing the amount.

        Example:
            >>> my_account.deposit(100)
            100.0
        """
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account balance.

        Args:
          self (object): The object instance.
          amount (float): The amount to be withdrawn.

        Returns:
          float: The updated account balance after withdrawal. If there are insufficient funds, returns None and prints an error message instead.

        Raises:
          ValueError: If the amount is greater than the available balance, it raises a ValueError with a message indicating 'Insufficient funds'.
        """
        if amount > self.balance:
            print('Insufficient funds')
            return
        self.balance -= amount
        return self.balance

def create_account(name, initial_deposit):
    """
    Creates a new bank account with the given name and initial deposit.

    Args:
        name (str): The name of the account holder.
        initial_deposit (float): The initial amount deposited into the account.

    Returns:
        BankAccount: A new BankAccount object representing the created account.
    """
    account = BankAccount(name, initial_deposit)
    return account

def transfer_funds(source_account, target_account, amount):
    """
    Transfers funds from one account to another.

    Args:
        source_account (object): The account to withdraw funds from.
        target_account (object): The account to deposit funds into.
        amount (int or float): The amount of funds to transfer.

    Returns:
        None if the transfer is successful, otherwise an error message.

    Raises:
        Exception: If the withdrawal or deposit operation fails.
    """
    if source_account.withdraw(amount) is not None:
        target_account.deposit(amount)
alice_account = create_account('Alice', 1000)
bob_account = create_account('Bob', 500)
print(f"Alice's initial balance: {alice_account.balance}")
print(f"Bob's initial balance: {bob_account.balance}")
transfer_funds(alice_account, bob_account, 200)
print(f"Alice's balance after transfer: {alice_account.balance}")
print(f"Bob's balance after transfer: {bob_account.balance}")