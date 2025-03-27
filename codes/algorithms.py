# algorithms.py: Contains deadlock detection, prevention, and recovery functions
import numpy as np
import networkx as nx

class DeadlockToolkit:
    def __init__(self, num_processes, num_resources):
        self.num_processes = num_processes
        self.num_resources = num_resources
        self.allocation = np.zeros((num_processes, num_resources), dtype=int)
        self.request = np.zeros((num_processes, num_resources), dtype=int)
        self.available = np.zeros(num_resources, dtype=int)
        self.max_demand = np.zeros((num_processes, num_resources), dtype=int)

    def set_initial_state(self, allocation, max_demand, available):
        """Initialize the system state."""
        self.allocation = np.array(allocation)
        self.max_demand = np.array(max_demand)
        self.available = np.array(available)
        self.request = np.zeros((self.num_processes, self.num_resources), dtype=int)

    def bankers_safety_check(self):
        """Check safety using Banker's Algorithm and return safe sequence."""
        temp_allocation = self.allocation.copy()
        temp_need = self.max_demand - temp_allocation
        work = self.available.copy()
        finished = [False] * self.num_processes
        safe_sequence = []

        while False in finished:
            found = False
            for p in range(self.num_processes):
                if not finished[p] and (temp_need[p] <= work).all():
                    work += temp_allocation[p]
                    finished[p] = True
                    safe_sequence.append(p)
                    found = True
            if not found:
                return False, "System is unsafe: No safe sequence exists."
        
        return True, f"System is safe. Safe sequence: {safe_sequence}"

    def detect_deadlock(self):
        """Detect deadlocks using resource allocation graph."""
        G = nx.DiGraph()
        for p in range(self.num_processes):
            G.add_node(f"P{p}")
        for r in range(self.num_resources):
            G.add_node(f"R{r}")
        
        for p in range(self.num_processes):
            for r in range(self.num_resources):
                if self.allocation[p][r] > 0:
                    G.add_edge(f"R{r}", f"P{p}")
                if self.request[p][r] > 0:
                    G.add_edge(f"P{p}", f"R{r}")

        cycles = list(nx.simple_cycles(G))
        return len(cycles) > 0, cycles if cycles else "No cycles detected"

    def recover_deadlock(self):
        """Recover from deadlock by terminating a process."""
        has_deadlock, _ = self.detect_deadlock()
        if not has_deadlock:
            return "No deadlock to recover from."
        resource_usage = self.allocation.sum(axis=1)
        process_to_kill = np.argmin(resource_usage)
        self.available += self.allocation[process_to_kill]
        self.allocation[process_to_kill] = 0
        return f"Recovered: Terminated P{process_to_kill}"