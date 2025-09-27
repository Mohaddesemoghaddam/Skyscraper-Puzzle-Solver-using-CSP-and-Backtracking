from typing import Any, List, Tuple
from CSP import CSP


class Solver:
    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, MAC: bool = False):
        self.csp = csp
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.MAC = MAC
        self.size = int(len(self.csp.variables) ** 0.5)  

    def backtrack_solver(self) -> dict | None:
        
        if self.csp.is_complete():
            return self.csp.assignments

        current_var = self.pick_variable()  

        for val in self.get_ordered_values(current_var): 
            if self.csp.is_consistent(current_var, val):
                self.csp.assign(current_var, val)
                if self.MAC:
                    removed_values = self.apply_MAC(current_var, val)
                result = self.backtrack_solver()
                if result:
                    return result
                self.csp.un_assign(current_var)
                if self.MAC:
                    self.csp.restore_domain(removed_values)

        return None

    def pick_variable(self) -> Any:
        """Select a variable using MRV or a default order."""
        if self.variable_heuristic:
            return self.apply_MRV(self.csp.unassigned_var)
        return self.csp.unassigned_var[0]

    def get_ordered_values(self, variable: Any) -> List[Any]:
        """Order domain values using LCV or default order."""
        if self.domain_heuristic:
            return self.apply_LCV(variable)
        return self.csp.variables[variable]

    def apply_MRV(self, variables: List[Any]) -> Any:
        """Select the variable with the fewest remaining values."""
        return min(variables, key=lambda var: len(self.csp.variables[var]))

    def apply_LCV(self, variable: Any) -> List[Any]:
        """Order values based on the least constraining value."""
        return sorted(
            self.csp.variables[variable],
            key=lambda val: self.calculate_constraints(variable, val),  
        )

    def calculate_constraints(self, variable: Any, value: Any) -> int:
        """Count the number of constraints a value imposes."""
        count = 0
        for constraint in self.csp.var_constraints[variable]:
            for other_var in constraint[1]:
                if value in self.csp.variables[other_var]:
                    count += 1
        return count

    def apply_MAC(self, variable: Any, value: Any) -> List[Tuple[Any, Any]]:
        """Apply MAC to prune inconsistent domain values."""
        queue = [(variable, var) for var in self.csp.variables if var != variable]
        removed_values = []
        while queue:
            x, y = queue.pop(0)
            if self.binary_arc_reduce(x, y):
                removed_values.append((x, y))
        return removed_values

    def binary_arc_reduce(self, x: Any, y: Any) -> bool:
        """Reduce domain values to maintain arc consistency."""
        removed = False
        for val in self.csp.variables[x]: 
            if not any(self.csp.is_consistent(x, y_val) for y_val in self.csp.variables[y]):
                self.csp.variables[x].remove(val)
                removed = True
        return removed



