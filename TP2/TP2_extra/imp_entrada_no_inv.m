


opts= bodeoptions('cstprefs');
opts.FreqUnits='Hz';
opts.PhaseVisible='off';
opts.MagUnits= 'abs';
bode(tf(12700, 1), opts, 'r');
h = findobj(gcf,'type','line');
set(h,'linewidth',2);

hold on

opts2= bodeoptions('cstprefs');
opts2.FreqUnits='Hz';
opts2.PhaseVisible='off';
opts2.MagUnits= 'abs';
bode(tf(12700, 1), opts2, 'g');
h = findobj(gcf,'type','line');
set(h,'linewidth',2);

opts3= bodeoptions('cstprefs');
opts3.FreqUnits='Hz';
opts3.PhaseVisible='on';
opts3.MagUnits= 'abs';
bode(tf(127000, 1), opts3, 'b');
h = findobj(gcf,'type','line');
set(h,'linewidth',2);



title('Impedancia de entrada'); 
legend('Caso 1','Caso 2','Caso 3' );
