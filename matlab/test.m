x = randn(1000,3); 
[counts, centers] = hist(x, 100);
stairs(centers, counts)