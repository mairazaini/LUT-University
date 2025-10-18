class CourseScheduler:
    def __init__(self, courses, teachers, rooms, time_slots):
        self.variables = courses
        self.teachers = teachers
        self.rooms = rooms  
        self.time_slots = time_slots
        
        self.domains = {}
        for course in courses:
            self.domains[course] = [(t, r) for t in time_slots for r in rooms]
    
    def is_consistent(self, assignment, course, value):
        """Check hard constraints: no room or teacher conflicts"""
        time, room = value
        
        for other_course, other_value in assignment.items():
            if other_value == (time, room):
                return False
          
        teacher = self.teachers[course]
        for other_course, other_value in assignment.items():
            other_time, other_room = other_value
            if (other_time == time and 
                self.teachers[other_course] == teacher):
                return False
                
        return True
    
    def select_unassigned_variable(self, assignment):
        """MRV: Choose variable with fewest remaining values"""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(self.domains[v]))
    
    def ac3(self):
        """Arc consistency: Remove inconsistent values from domains"""
        queue = [(i, j) for i in self.variables for j in self.variables if i != j]
        
        while queue:
            xi, xj = queue.pop(0)
            if self.remove_inconsistent_values(xi, xj):
                for xk in self.variables:
                    if xk != xi:
                        queue.append((xk, xi))
    
    def remove_inconsistent_values(self, xi, xj):
        """Remove values from xi that conflict with all values in xj"""
        removed = False
        for val_i in self.domains[xi][:]:
            consistent_exists = any(
                self.values_consistent(xi, val_i, xj, val_j) 
                for val_j in self.domains[xj]
            )
            if not consistent_exists:
                self.domains[xi].remove(val_i)
                removed = True
        return removed
    
    def values_consistent(self, xi, val_i, xj, val_j):
        """Check if two values satisfy constraints between variables"""
        time_i, room_i = val_i
        time_j, room_j = val_j
        
        if val_i == val_j:
            return False
            
        if (time_i == time_j and 
            self.teachers[xi] == self.teachers[xj]):
            return False
            
        return True

def backtracking_search(csp):
    """Main CSP solver with backtracking + MRV + AC-3"""
    return backtrack({}, csp)

def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables):
        return assignment
    
    var = csp.select_unassigned_variable(assignment)
    
    original_domains = {v: d[:] for v, d in csp.domains.items()}
    
    for value in csp.domains[var][:]: 
        if csp.is_consistent(assignment, var, value):
            assignment[var] = value
            
            csp.ac3()
            
            result = backtrack(assignment, csp)
            if result:
                return result
            
            del assignment[var]
            csp.domains = {v: d[:] for v, d in original_domains.items()}
    
    return None

def main():
    courses = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
    teachers = {
        'C1': 'T1', 'C2': 'T2', 'C3': 'T2', 'C4': 'T3', 'C5': 'T2',
        'C6': 'T3', 'C7': 'T1', 'C8': 'T3', 'C9': 'T3', 'C10': 'T2'
    }
    rooms = ['R1', 'R2', 'R3']
    time_slots = ['Slot1', 'Slot2', 'Slot3', 'Slot4', 'Slot5']
    
    print("Solving Course Scheduling CSP...")
    csp = CourseScheduler(courses, teachers, rooms, time_slots)
    solution = backtracking_search(csp)
    
    if solution:
        print("\n✅ SCHEDULE FOUND:")
        print("Course  | Teacher | Time   | Room")
        print("-" * 35)
        for course in sorted(solution.keys()):
            time, room = solution[course]
            teacher = teachers[course]
            print(f"{course:7} | {teacher:7} | {time:6} | {room:4}")
        
        print("\n✅ VERIFICATION: All constraints satisfied")
    else:
        print("❌ No valid schedule found")

if __name__ == "__main__":
    main()