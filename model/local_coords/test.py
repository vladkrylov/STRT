from loader import load_event, display_event

ev = load_event("/home/vlad/Program_Files/ilcsoft/marlintpc/workspace/25_Run_000025_170215_15-14-32/run_000025_data_000075_170215_15-14-49.txt"
               , max_hits_per_chip=4000
               )
display_event(ev)
