function f = good_bad_compare(good_param, bad_param, nbins)
f = figure();
all_param_values = [good_param, bad_param];
xmin = min(all_param_values);
xmax = max(all_param_values);

binning = linspace(xmin, xmax, nbins);
[good_counts, ~] = hist(good_param, binning);
[bad_counts, ~] = hist(bad_param, binning);

% normalization
good_counts = good_counts / max(good_counts);
bad_counts = bad_counts / max(bad_counts);

stairs(binning, good_counts, 'r')
hold on
stairs(binning, bad_counts, 'b')
hold off
grid on

legend('Good', 'Bad');
set(f, 'color', 'w');

end