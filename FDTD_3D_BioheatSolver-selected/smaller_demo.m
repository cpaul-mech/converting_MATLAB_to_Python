clear all
close all
clc

load('DemoModel.mat')
% Need T0, initial temperature condition
% We say that everything starts at temperature of 0 for a datum.
% Modl = Modl(1:4,1:4,1:4);
T0 = zeros(size(Modl),'single');
%convert Vox to m, given in mm.
Vox = Vox/1000;
dt = 0.05; %seconds
%need HT and CT, same size as nFZ
HT = path(end-2); %or position 7
CT = path(end-1);
wType = 1; % for uniform perfusion
tacq = 1; % aquisition time.
Tb= 0; 
BC = 0; %adiabatic, no energy escapes out of the edges
% the file is optional. 
% Q = Q(1:4,1:4,1:4);
nFZ= 1;

[TEMPS,time]=Calc_TEMPS_v04S(Modl,T0,Vox,dt,HT,CT,Props_rho,Props_k,Props_cp,wType,Props_w,Q,nFZ,tacq,Tb,BC);

plot(time,squeeze(TEMPS(71,71,60,:)))
% %TO slice the model and look at temp distribution use the command imagesc()
% imagesc(squeeze(TEMPS(71,:,:,11)),[0, 12])