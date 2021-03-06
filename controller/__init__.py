import ntpath

from model import Event, Track, Hit

class Controller():
    def __init__(self, my_model, my_view):
        self.model = my_model
        self.view = my_view
        if self.view:
            self.view.add_listener(self)
    
    def on_load_events(self, run_id, event_file_paths):
        if len(event_file_paths) == 0:
            return
        first_loaded_event = None
        for event_file_path in event_file_paths:
            ev = self.load_event(event_file_path)
            loaded = self.model.add_event(run_id, ev)
            if loaded and first_loaded_event is None:
                first_loaded_event = ev
        if self.view and first_loaded_event:
            run = self.model.get_run(run_id)
            i = run.events.index(first_loaded_event)
            is_first = i == 0
            is_last = i == len(run.events) - 1
            self.view.update_with_event(first_loaded_event, is_first=is_first, is_last=is_last)
    
    def load_event(self, file_path):
        with open(file_path) as infile:
            _, file_name = ntpath.split(file_path)
            ev_id = self.get_new_event_id(file_name, "Event", ".txt")
            ev = Event(ev_id, file_path)
            for line in infile:
                x, y = (float(n) for n in line.split())
                ev.add_hit(Hit(x, y))
        return ev
    
    def get_new_event_id(self, filename, ev_prefix, ev_suffix):
        if filename.startswith(ev_prefix) and filename.endswith(ev_suffix):
            try:
                return int(filename[len(ev_prefix): -len(ev_suffix)])
            except:
                if len(run.events) > 0:
                    return run.events[-1].id + 1
                else:
                    return 0
        return None
    
    def get_new_track_id(self, event_id):
        # TODO add missing ids pick
        event = self.model.get_event(event_id)
        existing_ids = [tr.id for tr in event.tracks]
        if len(existing_ids) == 0:
            return 0
        return max(existing_ids) + 1 
    
    def on_show_next_event(self, run_id, current_event):
        run = self.model.get_run(run_id)
        i = run.events.index(current_event)
        is_last = i == len(run.events) - 1
        if is_last:
            return
        next_event = run.events[i+1]
        is_last = (i+1) == len(run.events) - 1
        self.view.update_with_event(next_event, is_first=False, is_last=is_last)
    
    def on_show_previous_event(self, run_id, current_event):
        run = self.model.get_run(run_id)
        i = run.events.index(current_event)
        is_first = i == 0
        if is_first:
            return
        prev_event = run.events[i-1]
        is_first = (i-1) == 0
        self.view.update_with_event(prev_event, is_first=is_first, is_last=False)
    
    def show_event(self, run_id, event_id):
        run = self.model.get_run(run_id)
        event = self.model.get_event(run_id, event_id)
        if event is None:
            is_first, is_last = True, True
        else:
            is_first, is_last = self.get_event_first_last(run_id, event)
        self.view.update_with_event(event, is_first, is_last)
    
    def on_add_track(self, run_id, event_id):
        self.model.add_track(run_id, event_id)
        if self.view:
            event = self.model.get_event(run_id, event_id)
            is_first, is_last = self.get_event_first_last(run_id, event)
            self.view.update_with_event(event, is_first, is_last)
    
    def on_remove_track(self, event_id, track_id):
        return self.model.remove_track(event_id, track_id)
    
    def on_add_hits(self, run_id, event_id, track_id, selection_data):
        hit_indices = selection_data
        self.model.add_hits(run_id, event_id, track_id, hit_indices)
        if self.view:
            event = self.model.get_event(run_id, event_id)
            is_first, is_last = self.get_event_first_last(run_id, event)
            self.view.update_with_event(event, is_first, is_last)
    
    def on_remove_hits(self, run_id, event_id, track_id, selection_data):
        hit_indices = selection_data
        self.model.remove_hits(run_id, event_id, track_id, hit_indices)
        if self.view:
            event = self.model.get_event(run_id, event_id)
            is_first, is_last = self.get_event_first_last(run_id, event)
            self.view.update_with_event(event, is_first, is_last)

    def get_event_first_last(self, run_id, event):
        run = self.model.get_run(run_id)
        i = run.events.index(event)
        is_first = i == 0
        is_last = i == len(run.events) - 1
        return is_first, is_last
    
    def on_save_session(self, save_path):
        self.model.save_all(save_path)
    
    def on_load_session(self, load_path):
        run_id, event_id = self.model.load_all(load_path)
        event = self.model.get_event(run_id, event_id)
        is_first, is_last = self.get_event_first_last(run_id, event)
        self.view.update_run_table(self.model.runs)
        self.view.update_with_event(event, is_first=is_first, is_last=is_last)
    
    def on_dump_track(self, run_id, event_id, track_id):
        self.model.dump_track(run_id, event_id, track_id)
        
    def get_track_parameters(self):
        return self.model.get_track_parameters()
    
    def on_recalculate_track_parameters(self):
        self.model.calculate_track_parameters()
        
    def on_track_param_plot_update(self, parameter_name):
        param_distribution = self.model.get_param_distribution(parameter_name)
        self.view.update_track_param_plot(param_distribution)
        
    def on_event_Hough_transform(self, event_id):
        HT, lines = self.model.Hough_transform(event_id)
        self.view.update_Hough_transform_canvas(HT, lines)
        self.view.update_with_event(self.model.get_event(event_id))
        
    def on_reconstruct_all_events(self, run_id, parameters):
        self.model.analyze_all(run_id, parameters)
        run = self.model.get_run(run_id)
        if self.view:
            self.view.update_with_event(run.events[0])
        
    def on_event_fast_Hough_transform(self, run_id, event_id, parameters):
        self.model.fast_Hough_transform(run_id, event_id, parameters)
        self.view.update_with_event(self.model.get_event(run_id, event_id))
        
    def on_track_Hough_transform(self, event_id, track_id):
        HT, lines = self.model.Hough_transform(event_id, track_id)
        self.view.update_Hough_transform_canvas(HT, lines)
    
    def on_save_all_pdf(run_id, self):
        run = self.model.get_run(run_id)
        for ev in run.events:
            is_first, is_last = self.get_event_first_last(run_id, ev)
            self.view.update_with_event(ev, is_first=is_first, is_last=is_last)
            self.view.save_pdf()

    def export_to_matlab(self, run_id):
        self.model.dump2matlab(run_id)
    
    def mark_good_track(self, run_id, event_id, track_id, is_good):
        self.model.mark_good_track(run_id, event_id, track_id, is_good)
    
    def on_plot_dEdx(self, run_id, gap, nbins):
        self.model.plot_dEdx(run_id, gap, nbins)

    def on_new_run(self, run_name):
        run_id = None
        run_id = self.model.new_run(run_name)
        if self.view:
            self.view.update_run_table(self.model.runs)
        return run_id
        
    def on_remove_run(self, run_id):
        run = self.model.get_run(run_id)
        if run in self.model.runs:
            self.model.runs.remove(run)
        self.view.update_run_table(self.model.runs)
        
    def on_run_name_changed(self, run_id, new_name):
        self.model.set_run_name(run_id, new_name)
        # currently this triggers the cellChanged signal and causes an infinite loop
        # disabled so far, but should be reimplemented
#         self.view.update_run_table(self.model.runs)

