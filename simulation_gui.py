import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random


class SimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modeling & Simulation Project - GUI")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f0f0")
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs for each simulation
        self.create_double_server_tab()
        self.create_single_server_tab()
        self.create_event_scheduling_tab()
        self.create_mn_inventory_tab()
        self.create_newspaper_tab()
        
    # ==================== DOUBLE SERVER SIMULATION ====================
    def create_double_server_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Double Server Simulation")
        
        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Applicants:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ds_num_applicants = ttk.Entry(input_frame, width=15)
        self.ds_num_applicants.insert(0, "10")
        self.ds_num_applicants.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Run Simulation", command=self.run_double_server).grid(row=0, column=2, padx=20, pady=5)
        
        # Results Frame
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Table
        table_frame = ttk.LabelFrame(results_frame, text="Simulation Results", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.ds_tree = ttk.Treeview(table_frame, 
                                     columns=("Cust", "RandArr", "InterArr", "Arrive", "RandServ", 
                                             "S1Time", "S1Begin", "S1End", "S2Time", "S2Begin", "S2End", "Wait", "SysTime"),
                                     show="headings",
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.ds_tree.yview)
        tree_scroll_x.config(command=self.ds_tree.xview)
        
        # Define headings
        headings = ["Cust", "RandArr", "InterArr", "Arrive", "RandServ", "S1 Time", "S1 Begin", "S1 End", 
                   "S2 Time", "S2 Begin", "S2 End", "Wait", "SysTime"]
        for col, heading in zip(self.ds_tree["columns"], headings):
            self.ds_tree.heading(col, text=heading)
            self.ds_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.ds_tree.pack(fill=tk.BOTH, expand=True)
        
        # Performance Measures
        perf_frame = ttk.LabelFrame(results_frame, text="Performance Measures", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.ds_performance = tk.Text(perf_frame, height=10, width=100, font=("Courier", 10))
        self.ds_performance.pack(fill=tk.X)
        
    def run_double_server(self):
        try:
            num_applicants = int(self.ds_num_applicants.get())
            
            # Clear previous results
            for item in self.ds_tree.get_children():
                self.ds_tree.delete(item)
            self.ds_performance.delete(1.0, tk.END)
            
            # Run simulation logic
            result_data, performance = self.double_server_simulation(num_applicants)
            
            # Populate table
            for row in result_data:
                self.ds_tree.insert("", tk.END, values=row)
            
            # Display performance measures
            self.ds_performance.insert(1.0, performance)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values.")
    
    def double_server_simulation(self, num_applicants):
        arrival_ranges = [(5, 0, 29), (10, 30, 69), (15, 70, 89), (20, 90, 99)]
        service_ranges_server1 = [(15, 0, 24), (20, 25, 64), (30, 65, 89), (45, 90, 99)]
        service_ranges_server2 = [(10, 0, 19), (15, 20, 59), (25, 60, 89), (35, 90, 99)]
        
        def map_rand_to_time(rnd, ranges):
            for time, low, high in ranges:
                if low <= rnd <= high:
                    return time
            return ranges[-1][0]
        
        # Lists to store data
        rand_arrival_digits = []
        interarrivals = []
        arrival_times = []
        rand_service_digits_1 = []
        rand_service_digits_2 = []
        service_durations_1 = []
        service_durations_2 = []
        service_begin_1 = []
        service_end_1 = []
        service_begin_2 = []
        service_end_2 = []
        waiting_times = []
        time_in_system = []
        
        server_1_end_time = 0
        server_2_end_time = 0
        total_idle_time_1 = 0
        total_idle_time_2 = 0
        
        # First customer
        rnd_arr = random.randint(0, 99)
        rand_arrival_digits.append(rnd_arr)
        interarrivals.append(0)
        arrival_times.append(0)
        
        rnd_serv_1 = random.randint(0, 99)
        serv_time_1 = map_rand_to_time(rnd_serv_1, service_ranges_server1)
        
        rand_service_digits_1.append(rnd_serv_1)
        rand_service_digits_2.append(0)
        service_durations_1.append(serv_time_1)
        service_durations_2.append(0)
        service_begin_1.append(0)
        waiting_times.append(0)
        server_1_end_time = serv_time_1
        service_end_1.append(server_1_end_time)
        service_begin_2.append(0)
        service_end_2.append(0)
        time_in_system.append(server_1_end_time - arrival_times[0])
        
        # Remaining customers
        for i in range(1, num_applicants):
            rnd_arr = random.randint(0, 99)
            rand_arrival_digits.append(rnd_arr)
            inter = map_rand_to_time(rnd_arr, arrival_ranges)
            interarrivals.append(inter)
            arrival = arrival_times[-1] + inter
            arrival_times.append(arrival)
            
            if server_1_end_time <= server_2_end_time:
                server_free_time = server_1_end_time
                if arrival < server_free_time:
                    start_time = server_free_time
                    wait = start_time - arrival
                else:
                    start_time = arrival
                    wait = 0
                    idle_time = arrival - server_free_time
                    total_idle_time_1 += idle_time
                
                rnd_serv_1 = random.randint(0, 99)
                serv_time_1 = map_rand_to_time(rnd_serv_1, service_ranges_server1)
                end_time = start_time + serv_time_1
                
                rand_service_digits_1.append(rnd_serv_1)
                service_durations_1.append(serv_time_1)
                service_begin_1.append(start_time)
                service_end_1.append(end_time)
                server_1_end_time = end_time
                
                rand_service_digits_2.append(0)
                service_durations_2.append(0)
                service_begin_2.append(0)
                service_end_2.append(0)
            else:
                server_free_time = server_2_end_time
                if arrival < server_free_time:
                    start_time = server_free_time
                    wait = start_time - arrival
                else:
                    start_time = arrival
                    wait = 0
                    idle_time = arrival - server_free_time
                    total_idle_time_2 += idle_time
                
                rnd_serv_2 = random.randint(0, 99)
                serv_time_2 = map_rand_to_time(rnd_serv_2, service_ranges_server2)
                end_time = start_time + serv_time_2
                
                rand_service_digits_2.append(rnd_serv_2)
                service_durations_2.append(serv_time_2)
                service_begin_2.append(start_time)
                service_end_2.append(end_time)
                server_2_end_time = end_time
                
                rand_service_digits_1.append(0)
                service_durations_1.append(0)
                service_begin_1.append(0)
                service_end_1.append(0)
            
            waiting_times.append(wait)
            time_in_system.append(end_time - arrival)
        
        # Format data for table
        result_data = []
        for i in range(num_applicants):
            rnd_serv = rand_service_digits_1[i] + rand_service_digits_2[i]
            result_data.append((
                i+1, rand_arrival_digits[i], interarrivals[i], arrival_times[i], rnd_serv,
                service_durations_1[i], service_begin_1[i], service_end_1[i],
                service_durations_2[i], service_begin_2[i], service_end_2[i],
                waiting_times[i], time_in_system[i]
            ))
        
        # Calculate performance measures
        total_time_horizon = max(server_1_end_time, server_2_end_time)
        total_service_time_1 = sum(service_durations_1)
        total_service_time_2 = sum(service_durations_2)
        total_service_time = total_service_time_1 + total_service_time_2
        avg_wait = sum(waiting_times) / num_applicants
        prob_wait = sum(1 for w in waiting_times if w > 0) / num_applicants
        server_utilization_1 = total_service_time_1 / total_time_horizon
        server_utilization_2 = total_service_time_2 / total_time_horizon
        system_utilization = total_service_time / (2 * total_time_horizon)
        avg_service = total_service_time / num_applicants
        avg_in_system = sum(time_in_system) / num_applicants
        total_idle_calc_1 = total_time_horizon - total_service_time_1
        total_idle_calc_2 = total_time_horizon - total_service_time_2
        prob_server_1_idle = total_idle_calc_1 / total_time_horizon
        prob_server_2_idle = total_idle_calc_2 / total_time_horizon
        
        performance = f"""Total Time Horizon (max end time): {total_time_horizon} minutes
Average waiting time: {avg_wait:.2f} minutes
Probability a customer waits: {prob_wait:.2f}

Server Utilization:
  Server 1 (Able): {server_utilization_1:.2f}
  Server 2 (Baker): {server_utilization_2:.2f}
  System Utilization (2 servers): {system_utilization:.2f}

Server Idle Probability:
  Server 1 (Able) Idle Prob: {prob_server_1_idle:.2f}
  Server 2 (Baker) Idle Prob: {prob_server_2_idle:.2f}

Average service time (across both servers): {avg_service:.2f} minutes
Average time in system: {avg_in_system:.2f} minutes"""
        
        return result_data, performance
    
    # ==================== SINGLE SERVER SIMULATION ====================
    def create_single_server_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Single Server Simulation")
        
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Applicants:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ss_num_applicants = ttk.Entry(input_frame, width=15)
        self.ss_num_applicants.insert(0, "10")
        self.ss_num_applicants.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Run Simulation", command=self.run_single_server).grid(row=0, column=2, padx=20, pady=5)
        
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_frame = ttk.LabelFrame(results_frame, text="Simulation Results", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.ss_tree = ttk.Treeview(table_frame,
                                     columns=("Cust", "RandArr", "InterArr", "Arrive", "RandServ", 
                                             "ServTime", "Start", "Wait", "End", "Idle", "InSystem"),
                                     show="headings",
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.ss_tree.yview)
        tree_scroll_x.config(command=self.ss_tree.xview)
        
        headings = ["Cust", "RandArr", "InterArr", "Arrive", "RandServ", "ServTime", "Start", "Wait", "End", "Idle", "InSystem"]
        for col, heading in zip(self.ss_tree["columns"], headings):
            self.ss_tree.heading(col, text=heading)
            self.ss_tree.column(col, width=90, anchor=tk.CENTER)
        
        self.ss_tree.pack(fill=tk.BOTH, expand=True)
        
        perf_frame = ttk.LabelFrame(results_frame, text="Performance Measures", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.ss_performance = tk.Text(perf_frame, height=8, width=100, font=("Courier", 10))
        self.ss_performance.pack(fill=tk.X)
    
    def run_single_server(self):
        try:
            num_applicants = int(self.ss_num_applicants.get())
            
            for item in self.ss_tree.get_children():
                self.ss_tree.delete(item)
            self.ss_performance.delete(1.0, tk.END)
            
            result_data, performance = self.single_server_simulation(num_applicants)
            
            for row in result_data:
                self.ss_tree.insert("", tk.END, values=row)
            
            self.ss_performance.insert(1.0, performance)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values.")
    
    def single_server_simulation(self, num_applicants):
        arrival_ranges = [(5, 0, 29), (10, 30, 69), (15, 70, 89), (20, 90, 99)]
        service_ranges = [(15, 0, 24), (20, 25, 64), (30, 65, 89), (45, 90, 99)]
        
        def map_rand_to_time(rnd, ranges):
            for time, low, high in ranges:
                if low <= rnd <= high:
                    return time
            return ranges[-1][0]
        
        rand_arrival_digits = []
        interarrivals = []
        arrival_times = []
        rand_service_digits = []
        service_durations = []
        service_start = []
        service_end = []
        waiting_times = []
        idle_times = []
        time_in_system = []
        
        # First applicant
        rnd_arr = random.randint(0, 99)
        rand_arrival_digits.append(rnd_arr)
        interarrivals.append(0)
        arrival_times.append(0)
        
        rnd_serv = random.randint(0, 99)
        rand_service_digits.append(rnd_serv)
        serv_time = map_rand_to_time(rnd_serv, service_ranges)
        service_durations.append(serv_time)
        service_start.append(0)
        waiting_times.append(0)
        service_end.append(serv_time)
        idle_times.append(0)
        time_in_system.append(serv_time - arrival_times[0])
        
        # Remaining customers
        for i in range(1, num_applicants):
            rnd_arr = random.randint(0, 99)
            rand_arrival_digits.append(rnd_arr)
            inter = map_rand_to_time(rnd_arr, arrival_ranges)
            interarrivals.append(inter)
            arrival = arrival_times[-1] + inter
            arrival_times.append(arrival)
            
            rnd_serv = random.randint(0, 99)
            rand_service_digits.append(rnd_serv)
            serv_time = map_rand_to_time(rnd_serv, service_ranges)
            service_durations.append(serv_time)
            
            if arrival < service_end[-1]:
                start = service_end[-1]
                wait = start - arrival
                idle = 0
            else:
                start = arrival
                wait = 0
                idle = arrival - service_end[-1]
            
            end = start + serv_time
            in_system = end - arrival
            
            service_start.append(start)
            waiting_times.append(wait)
            service_end.append(end)
            idle_times.append(idle)
            time_in_system.append(in_system)
        
        # Format data
        result_data = []
        for i in range(num_applicants):
            result_data.append((
                i+1, rand_arrival_digits[i], interarrivals[i], arrival_times[i],
                rand_service_digits[i], service_durations[i], service_start[i],
                waiting_times[i], service_end[i], idle_times[i], time_in_system[i]
            ))
        
        # Performance measures
        avg_wait = sum(waiting_times) / num_applicants
        prob_wait = sum(1 for w in waiting_times if w > 0) / num_applicants
        total_idle = sum(idle_times)
        total_time_horizon = service_end[-1] - arrival_times[0]
        server_utilization = (sum(service_durations) / (sum(service_durations) + total_idle)) if (sum(service_durations)+total_idle)>0 else 0
        prob_server_idle = total_idle / (sum(service_durations) + total_idle) if (sum(service_durations)+total_idle)>0 else 0
        avg_service = sum(service_durations) / num_applicants
        avg_in_system = sum(time_in_system) / num_applicants
        
        performance = f"""Average waiting time: {avg_wait:.2f} minutes
Probability someone waits: {prob_wait:.2f}
Server utilization (busy fraction): {server_utilization:.2f}
Probability server idle: {prob_server_idle:.2f}
Average service time: {avg_service:.2f} minutes
Average time in system: {avg_in_system:.2f} minutes"""
        
        return result_data, performance
    
    # ==================== EVENT SCHEDULING SIMULATION ====================
    def create_event_scheduling_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Event Scheduling")
        
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Customers:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.es_max_customers = ttk.Entry(input_frame, width=15)
        self.es_max_customers.insert(0, "10")
        self.es_max_customers.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Stop Time (minutes):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.es_stop_time = ttk.Entry(input_frame, width=15)
        self.es_stop_time.insert(0, "60")
        self.es_stop_time.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Run Simulation", command=self.run_event_scheduling).grid(row=0, column=4, padx=20, pady=5)
        
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_frame = ttk.LabelFrame(results_frame, text="Simulation Results", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.es_tree = ttk.Treeview(table_frame,
                                     columns=("Clock", "Event", "LQ", "LS", "FEL", "S", "Nd", "B", "MQ"),
                                     show="headings",
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.es_tree.yview)
        tree_scroll_x.config(command=self.es_tree.xview)
        
        headings = ["Clock", "Event", "LQ(t)", "LS(t)", "FEL (Type, Time)", "S", "Nd", "B", "MQ"]
        widths = [60, 100, 60, 60, 300, 60, 50, 60, 50]
        for col, heading, width in zip(self.es_tree["columns"], headings, widths):
            self.es_tree.heading(col, text=heading)
            self.es_tree.column(col, width=width, anchor=tk.CENTER)
        
        self.es_tree.pack(fill=tk.BOTH, expand=True)
        
        perf_frame = ttk.LabelFrame(results_frame, text="Performance Measures", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.es_performance = tk.Text(perf_frame, height=6, width=100, font=("Courier", 10))
        self.es_performance.pack(fill=tk.X)
    
    def run_event_scheduling(self):
        try:
            max_customers = int(self.es_max_customers.get())
            stop_time = int(self.es_stop_time.get())
            
            for item in self.es_tree.get_children():
                self.es_tree.delete(item)
            self.es_performance.delete(1.0, tk.END)
            
            result_data, performance = self.event_scheduling_simulation(max_customers, stop_time)
            
            for row in result_data:
                self.es_tree.insert("", tk.END, values=row)
            
            self.es_performance.insert(1.0, performance)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values.")
    
    def event_scheduling_simulation(self, max_customers, stop_time):
        def get_interarrival_time():
            return random.randint(1, 8)
        
        def get_service_time():
            return random.randint(1, 6)
        
        clock = 0
        server_status = 0
        queue_list = []
        S = 0.0
        B = 0.0
        Nd = 0
        MQ = 0
        last_event_time = 0
        customer_id_counter = 1
        event_list = []
        
        event_list.append({'type': 'A', 'time': 0, 'id': customer_id_counter})
        customer_id_counter += 1
        
        result_data = []
        
        while clock <= stop_time and Nd < max_customers:
            if not event_list:
                break
            
            event_list.sort(key=lambda x: x['time'])
            current_event = event_list.pop(0)
            
            if current_event['time'] > stop_time:
                remaining = stop_time - clock
                num_in_sys = len(queue_list) + server_status
                S += num_in_sys * remaining
                B += server_status * remaining
                clock = stop_time
                break
            
            time_since_last = current_event['time'] - last_event_time
            clock = current_event['time']
            last_event_time = clock
            
            B += server_status * time_since_last
            num_in_sys = len(queue_list) + server_status
            S += num_in_sys * time_since_last
            
            if len(queue_list) > MQ:
                MQ = len(queue_list)
            
            event_type = current_event['type']
            cust_id = current_event['id']
            
            if event_type == 'A':
                inter = get_interarrival_time()
                next_arr = clock + inter
                if next_arr <= stop_time + 20:
                    event_list.append({'type': 'A', 'time': next_arr, 'id': customer_id_counter})
                    customer_id_counter += 1
                
                if server_status == 0:
                    server_status = 1
                    serv = get_service_time()
                    dep_time = clock + serv
                    event_list.append({'type': 'D', 'time': dep_time, 'id': cust_id})
                else:
                    queue_list.append(cust_id)
            
            elif event_type == 'D':
                Nd += 1
                if len(queue_list) > 0:
                    next_cust = queue_list.pop(0)
                    server_status = 1
                    serv = get_service_time()
                    dep_time = clock + serv
                    event_list.append({'type': 'D', 'time': dep_time, 'id': next_cust})
                else:
                    server_status = 0
            
            event_list.sort(key=lambda x: x['time'])
            fel_str = ""
            for e in event_list[:5]:  # Limit FEL display
                fel_str += f"({e['type']},{e['time']}) "
            
            evt_display = f"{'Arr' if event_type=='A' else 'Dep'}(C{cust_id})"
            
            result_data.append((
                int(clock), evt_display, len(queue_list), server_status,
                fel_str, int(S), Nd, int(B), MQ
            ))
        
        if clock > 0:
            avg_q_len = (S - B) / clock
            utilization = B / clock
        else:
            avg_q_len = 0
            utilization = 0
        
        performance = f"""Total Simulation Time:   {clock} min
Total Departures (Nd):   {Nd}
Max Queue Length (MQ):   {MQ}
Server Utilization:      {utilization:.2f} ({(utilization*100):.1f}%)
Avg Queue Length:        {avg_q_len:.2f} customers"""
        
        return result_data, performance
    
    # ==================== M-N INVENTORY SIMULATION ====================
    def create_mn_inventory_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="M-N Inventory")
        
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Initial Inventory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.mn_initial_inv = ttk.Entry(input_frame, width=10)
        self.mn_initial_inv.insert(0, "12")
        self.mn_initial_inv.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Cycle Length (N):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.mn_cycle = ttk.Entry(input_frame, width=10)
        self.mn_cycle.insert(0, "7")
        self.mn_cycle.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Reorder Point (M):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.mn_reorder = ttk.Entry(input_frame, width=10)
        self.mn_reorder.insert(0, "6")
        self.mn_reorder.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Order Quantity:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mn_order_qty = ttk.Entry(input_frame, width=10)
        self.mn_order_qty.insert(0, "10")
        self.mn_order_qty.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Simulation Days:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.mn_num_days = ttk.Entry(input_frame, width=10)
        self.mn_num_days.insert(0, "28")
        self.mn_num_days.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Run Simulation", command=self.run_mn_inventory).grid(row=1, column=4, padx=20, pady=5)
        
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_frame = ttk.LabelFrame(results_frame, text="Simulation Results", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.mn_tree = ttk.Treeview(table_frame,
                                     columns=("Cycle", "Day", "BeginInv", "RndDem", "Demand", 
                                             "EndInv", "Shortage", "OrderQty", "RndLead", "DaysUntil"),
                                     show="headings",
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.mn_tree.yview)
        tree_scroll_x.config(command=self.mn_tree.xview)
        
        headings = ["Cycle", "Day", "BeginInv", "RndDem", "Demand", "EndInv", "Shortage", "OrderQty", "RndLead", "DaysUntil"]
        for col, heading in zip(self.mn_tree["columns"], headings):
            self.mn_tree.heading(col, text=heading)
            self.mn_tree.column(col, width=90, anchor=tk.CENTER)
        
        self.mn_tree.pack(fill=tk.BOTH, expand=True)
        
        perf_frame = ttk.LabelFrame(results_frame, text="Performance Measures", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.mn_performance = tk.Text(perf_frame, height=4, width=100, font=("Courier", 10))
        self.mn_performance.pack(fill=tk.X)
    
    def run_mn_inventory(self):
        try:
            initial_inv = int(self.mn_initial_inv.get())
            cycle_length = int(self.mn_cycle.get())
            reorder_point = int(self.mn_reorder.get())
            order_quantity = int(self.mn_order_qty.get())
            num_days = int(self.mn_num_days.get())
            
            for item in self.mn_tree.get_children():
                self.mn_tree.delete(item)
            self.mn_performance.delete(1.0, tk.END)
            
            result_data, performance = self.mn_inventory_simulation(
                initial_inv, cycle_length, reorder_point, order_quantity, num_days)
            
            for row in result_data:
                self.mn_tree.insert("", tk.END, values=row)
            
            self.mn_performance.insert(1.0, performance)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values.")
    
    def mn_inventory_simulation(self, initial_inv, cycle_length, reorder_point, order_quantity, num_days):
        def get_demand(rnd):
            if 1 <= rnd <= 33: return 0
            elif 34 <= rnd <= 58: return 1
            elif 59 <= rnd <= 78: return 2
            elif 79 <= rnd <= 90: return 3
            else: return 4
        
        def get_lead_time(rnd):
            if 1 <= rnd <= 30: return 1
            elif 31 <= rnd <= 80: return 2
            else: return 3
        
        current_inventory_pos = initial_inv
        order_arrival_day = -1
        order_amount_coming = 0
        table_data = []
        
        for day in range(1, num_days + 1):
            cycle_num = ((day - 1) // cycle_length) + 1
            day_in_cycle = day % cycle_length
            if day_in_cycle == 0:
                day_in_cycle = cycle_length
            
            if day == order_arrival_day:
                current_inventory_pos += order_amount_coming
                order_arrival_day = -1
            
            begin_inv_display = max(0, current_inventory_pos)
            
            rnd_dem = random.randint(1, 100)
            demand = get_demand(rnd_dem)
            
            current_inventory_pos -= demand
            
            if current_inventory_pos >= 0:
                end_inv_display = current_inventory_pos
                shortage_display = 0
            else:
                end_inv_display = 0
                shortage_display = abs(current_inventory_pos)
            
            is_review_day = (day % cycle_length == 0)
            
            order_placed_str = ""
            rnd_lead_str = ""
            days_until_str = ""
            
            if order_arrival_day != -1:
                days_left = order_arrival_day - day - 1
                if days_left < 0:
                    days_left = 0
                days_until_str = str(days_left)
            
            if is_review_day:
                if current_inventory_pos <= reorder_point and order_arrival_day == -1:
                    rnd_lead = random.randint(1, 100)
                    lead_time = get_lead_time(rnd_lead)
                    order_amount_coming = order_quantity
                    order_arrival_day = day + lead_time + 1
                    order_placed_str = str(order_quantity)
                    rnd_lead_str = str(rnd_lead)
                    days_until_str = str(lead_time)
            
            row = (
                cycle_num if day_in_cycle == 1 else "",
                day_in_cycle,
                begin_inv_display,
                rnd_dem,
                demand,
                end_inv_display,
                shortage_display if shortage_display > 0 else "",
                order_placed_str,
                rnd_lead_str,
                days_until_str
            )
            table_data.append(row)
        
        total_end_inv = sum(row[5] for row in table_data)
        days_with_shortage = sum(1 for row in table_data if row[6] != "")
        
        avg_end_inv = total_end_inv / num_days
        shortage_percent = (days_with_shortage / num_days) * 100
        
        performance = f"""Average Ending Inventory: {avg_end_inv:.2f} units
Shortage Condition Existed: {days_with_shortage} days ({shortage_percent:.1f}%)"""
        
        return table_data, performance
    
    # ==================== NEWSPAPER SIMULATION ====================
    def create_newspaper_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Newspaper Simulation")
        
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Newspapers:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.np_num_papers = ttk.Entry(input_frame, width=15)
        self.np_num_papers.insert(0, "70")
        self.np_num_papers.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Simulation Days:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.np_num_days = ttk.Entry(input_frame, width=15)
        self.np_num_days.insert(0, "20")
        self.np_num_days.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Run Simulation", command=self.run_newspaper).grid(row=0, column=4, padx=20, pady=5)
        
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_frame = ttk.LabelFrame(results_frame, text="Simulation Results", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.np_tree = ttk.Treeview(table_frame,
                                     columns=("Day", "RndType", "Type", "RndDem", "Dem", 
                                             "Revenue", "LostProf", "Salvage", "Profit"),
                                     show="headings",
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.np_tree.yview)
        tree_scroll_x.config(command=self.np_tree.xview)
        
        headings = ["Day", "RndType", "Type", "RndDem", "Dem", "Revenue", "LostProf", "Salvage", "Profit"]
        for col, heading in zip(self.np_tree["columns"], headings):
            self.np_tree.heading(col, text=heading)
            self.np_tree.column(col, width=90, anchor=tk.CENTER)
        
        self.np_tree.pack(fill=tk.BOTH, expand=True)
        
        perf_frame = ttk.LabelFrame(results_frame, text="Performance Measures", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.np_performance = tk.Text(perf_frame, height=6, width=100, font=("Courier", 10))
        self.np_performance.pack(fill=tk.X)
    
    def run_newspaper(self):
        try:
            num_papers = int(self.np_num_papers.get())
            num_days = int(self.np_num_days.get())
            
            for item in self.np_tree.get_children():
                self.np_tree.delete(item)
            self.np_performance.delete(1.0, tk.END)
            
            result_data, performance = self.newspaper_simulation(num_papers, num_days)
            
            for row in result_data:
                self.np_tree.insert("", tk.END, values=row)
            
            self.np_performance.insert(1.0, performance)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values.")
    
    def newspaper_simulation(self, num_papers, num_days):
        COST_PER_PAPER = 0.33
        SELLING_PRICE = 0.50
        SALVAGE_VALUE = 0.05
        LOST_PROFIT_PER_UNIT = SELLING_PRICE - COST_PER_PAPER
        daily_cost = num_papers * COST_PER_PAPER
        
        def get_newsday_type(rnd):
            if 1 <= rnd <= 35: return "Good"
            elif 36 <= rnd <= 80: return "Fair"
            else: return "Poor"
        
        def get_demand(newsday_type, rnd):
            if newsday_type == "Good":
                if 1 <= rnd <= 3: return 40
                elif 4 <= rnd <= 8: return 50
                elif 9 <= rnd <= 23: return 60
                elif 24 <= rnd <= 43: return 70
                elif 44 <= rnd <= 78: return 80
                elif 79 <= rnd <= 93: return 90
                else: return 100
            elif newsday_type == "Fair":
                if 1 <= rnd <= 10: return 40
                elif 11 <= rnd <= 28: return 50
                elif 29 <= rnd <= 68: return 60
                elif 69 <= rnd <= 88: return 70
                elif 89 <= rnd <= 96: return 80
                elif 97 <= rnd <= 100: return 90
                else: return 90
            else:
                if 1 <= rnd <= 44: return 40
                elif 45 <= rnd <= 66: return 50
                elif 67 <= rnd <= 82: return 60
                elif 83 <= rnd <= 94: return 70
                else: return 80
        
        total_revenue = 0.0
        total_lost_profit = 0.0
        total_salvage = 0.0
        total_daily_profit = 0.0
        table_data = []
        
        for day in range(1, num_days + 1):
            rnd_type = random.randint(1, 100)
            day_type = get_newsday_type(rnd_type)
            
            rnd_dem = random.randint(1, 100)
            demand = get_demand(day_type, rnd_dem)
            
            units_sold = min(demand, num_papers)
            revenue = units_sold * SELLING_PRICE
            
            if demand > num_papers:
                excess_demand = demand - num_papers
                lost_profit = excess_demand * LOST_PROFIT_PER_UNIT
            else:
                lost_profit = 0.0
            
            if num_papers > demand:
                unsold = num_papers - demand
                salvage = unsold * SALVAGE_VALUE
            else:
                salvage = 0.0
            
            daily_profit = revenue - daily_cost - lost_profit + salvage
            
            total_revenue += revenue
            total_lost_profit += lost_profit
            total_salvage += salvage
            total_daily_profit += daily_profit
            
            table_data.append((
                day, rnd_type, day_type, rnd_dem, demand,
                f"{revenue:.2f}", f"{lost_profit:.2f}", f"{salvage:.2f}", f"{daily_profit:.2f}"
            ))
        
        performance = f"""Total Revenue:       ${total_revenue:.2f}
Total Cost:          ${(daily_cost * num_days):.2f}  ({num_papers} papers * ${COST_PER_PAPER} * {num_days} days)
Total Lost Profit:   ${total_lost_profit:.2f}
Total Salvage:       ${total_salvage:.2f}
Net Profit:          ${total_daily_profit:.2f}"""
        
        return table_data, performance


def main():
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
