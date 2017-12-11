function mpv = dEdx(run_id)

data_mat_file = ['Run' num2str(run_id) 'tracks.mat'];
% data_mat_file = ['Run' num2str(run_id) 'tracks_manual.mat'];
load(data_mat_file);
% the_good_the_bad_and_the_ugly(data_mat_file, run_id, false)

n_tracks = size(lincoords, 1);

gap_length = 2;  % mm

max_n_gaps = fix(max(lincoords(:)) / gap_length);
dN = NaN(n_tracks, max_n_gaps);
for i=1:n_tracks
    track_lincoords = lincoords(i,:);
    n_gaps = fix(max(track_lincoords) / gap_length);
    lin_coord_bin_centers = gap_length*(1:n_gaps) - gap_length/2;
    track_lincoords(track_lincoords > n_gaps*gap_length) = NaN;
    [dN_per_gap, ~] = hist(track_lincoords, lin_coord_bin_centers);
    dN(i, 1:n_gaps) = dN_per_gap;
end

[counts, centers] = hist(dN(:), max(dN(:)*gap_length));
figure()
centers = centers / gap_length;
stairs(centers, counts)
title(['Run ' num2str(run_id)])
xlabel('dN_{e}/dx, [electrons/mm]')
ylabel('Counts')
grid on

end
