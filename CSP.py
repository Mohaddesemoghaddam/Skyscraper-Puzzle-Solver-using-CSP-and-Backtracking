from collections import deque
from typing import Callable, List, Tuple, Any


class CSP:
    """
    Represents a Constraint Satisfaction Problem (CSP).
    Attributes:
        variables (dict): A dictionary that maps variables to their domains.
        constraints (list): A list of constraints in the form of [constraint_func, variables].
        unassigned_variables (list): A list of unassigned variables.
        variable_constraints (dict): A dictionary that maps variables to their associated constraints.
    """

    def __init__(self) -> None:
        """
        Initializes a Constraint Satisfaction Problem (CSP) object.
        """
        self.variables = {}
        self.constraints = []
        self.unassigned_variables = [] 
        self.variable_constraints = {}  
        self.assignments = {}
        self.assignment_count = 0  

    def add_constraint(self, constraint_func: Callable, involved_variables: List) -> None:
        """
        Adds a constraint to the CSP.
        Args:
            constraint_func (function): The constraint function to be added.
            involved_variables (list): The variables involved in the constraint.
        """
        self.constraints.append((constraint_func, involved_variables))
        for variable in involved_variables:
            if variable not in self.variable_constraints:
                self.variable_constraints[variable] = []
            self.variable_constraints[variable].append((constraint_func, involved_variables))

    def add_variable(self, variable: Any, domain: List) -> None:
        """
        Adds a variable to the CSP with its domain.
        Args:
            variable: The variable to be added.
            domain: The domain of the variable.
        """
        self.variables[variable] = domain[:]
        self.unassigned_variables.append(variable)
        self.assignments[variable] = None

    def assign(self, variable: Any, value: Any) -> None:
        """
        Assigns a value to a variable in the CSP.
        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.
        """
        self.assignments[variable] = value
        self.unassigned_variables.remove(variable)

    def un_assign(self, variable: Any) -> None:
        """
        Unassign a variable and restores it to the unassigned list.
        Args:
            variable (any): The variable to be unassigned.
        """
        self.assignments[variable] = None
        self.unassigned_variables.append(variable)

    def is_consistent(self, variable: Any, value: Any) -> bool:
        """
        Checks if assigning a value to a variable violates any constraints.
        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.
        Returns:
            bool: True if the assignment is consistent with the constraints, False otherwise.
        """
        for constraint, involved_variables in self.variable_constraints.get(variable, []):

            temp_assignments = self.assignments.copy()
            temp_assignments[variable] = value

            if not constraint(temp_assignments):
                return False
        return True

    def is_complete(self) -> bool:
        """
        Checks if the CSP is complete, i.e., all variables have been assigned.
        Returns:
            bool: True if the CSP is complete, False otherwise.
        """
        return all(value is not None for value in self.assignments.values())

    def restore_domain(self, removed_values: List[Tuple[Any, Any]]) -> None:
        """
        Restores domain values that were removed during inference.
        Args:
            removed_values (list): A list of domain values to be restored.
        """
        for variable, value in removed_values:
            self.variables[variable].append(value)

    def apply_arc_consistency(self) -> List[Tuple[Any, Any]]:
        """
        Applies arc consistency to the CSP to reduce domain values.
        Returns:
            List[Tuple[Any, Any]]: A list of removed values for restoration.
        """
        arc_queue = deque([(x, y) for x in self.variables for y in self.variables if x != y]) 
        removed_values = []

        while arc_queue:
            x, y = arc_queue.popleft()
            if self.revise(x, y):
                if not self.variables[x]:
                    return []
                for z in self.variables:
                    if z != x and z != y:
                        arc_queue.append((z, x))  

        return removed_values

    def revise(self, x: Any, y: Any) -> bool:
        """
        Revises the domain of variable x to ensure consistency with y.
        Args:
            x (Any): The first variable.
            y (Any): The second variable.
        Returns:
            bool: True if the domain of x was revised, False otherwise.
        """
        modified = False  
        for value in self.variables[x][:]: 
            if not any(self.is_consistent(x, domain_value) for domain_value in self.variables[y]):
                self.variables[x].remove(value)
                modified = True
        return modified
