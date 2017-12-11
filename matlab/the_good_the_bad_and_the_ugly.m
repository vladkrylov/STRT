function the_good_the_bad_and_the_ugly(data_mat_file, run_id, save_cut_figures)
load(data_mat_file);

%% length
f_length = good_bad_compare(good_tracks_length, bad_tracks_length, 100);
axes = findobj(f_length,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'Track length, mm')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% Nhits
f_Nhits = good_bad_compare(good_tracks_Nhits, bad_tracks_Nhits, 100);
axes = findobj(f_Nhits,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'Number of track hits')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% rho
f_rho = good_bad_compare(good_tracks_rho, bad_tracks_rho, 100);
axes = findobj(f_rho,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', '\rho, mm')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% theta
f_theta = good_bad_compare(good_tracks_theta, bad_tracks_theta, 50);
axes = findobj(f_theta,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', '\theta, rad')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% x0
f_x0 = good_bad_compare(good_tracks_x0, bad_tracks_x0, 50);
axes = findobj(f_x0,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'x_{0}, mm')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% y0
f_y0 = good_bad_compare(good_tracks_y0, bad_tracks_y0, 50);
axes = findobj(f_y0,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'y_{0}, mm')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% R^2
f_R2 = good_bad_compare(good_tracks_R2, bad_tracks_R2, 100);
axes = findobj(f_R2,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'R^{2}, mm^2')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

%% density
good_dens = good_tracks_Nhits ./ good_tracks_length;
bad_dens = bad_tracks_Nhits ./ bad_tracks_length;

f_dens = good_bad_compare(good_dens, bad_dens, 100);
axes = findobj(f_dens,'type','axe');
set(get(axes, 'title'), 'string', ['Run ' num2str(run_id)])
set(get(axes, 'xlabe'), 'string', 'Hits density, 1/mm')
set(get(axes, 'ylabe'), 'string', 'Number of tracks (normalized)')

if save_cut_figures
    print(f_length, 'length_cut','-dpng')
    print(f_Nhits, 'Nhits_cut','-dpng')
    print(f_rho, 'rho_cut','-dpng')
    print(f_theta, 'theta_cut','-dpng')
    print(f_x0, 'x0_cut','-dpng')
    print(f_y0, 'y0_cut','-dpng')
    print(f_R2, 'R2_cut','-dpng')
    print(f_dens, 'dens_cut','-dpng')
end

end
