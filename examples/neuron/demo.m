% Simulation of Tap Withdrawal (TW) circuit  of C Elegans
% Wicks et al. model
% ID of Neurons: 
    % AVM: 1
    % ALM: 2
    % PLM: 3
    % AVD: 4
    % AVA: 5
    % PVC: 6
    % AVB: 7
    % PVD: 8
    % DVA: 9
% Touch sensory neurons: PLM, ALM and AVM. Stimulus is applied only on
% these neurons.  
stimID=[1,3]; knockedOut=0;
%Input: 
% KnockedOut: The ID(s) of the neurons which are to be knockedout
% stimID: The ID(s) of the neurons to which stimulus will be applied
%% Declare global variable
global IStim;
global W_gap;
global W_syn;
global Cap;
global E_syn;
global Res;
global V_eq;
global dt;
%% Network Connectivity Matrices of TW Circuit (Adjacency matrix)
load 'Connectivity_matrix_new.mat'; % Will Load W_GAP and W_SYN
%% Membrane Properties
% Capacittance
Cap = [5;9.1;9.1;14;15;16;14;16; 15]*1e-12;
% Resistance
Res = [30;16;16;11;10;9.4;11; 9.4; 10]*1e9;
% Reverse Potential of Neuron based on Polarities
E_syn = [-0.048;-0.048;-0.048;0;-0.048;0;-0.048;-0.048;-0.048];
%% Loading initial state from file
load 'InitialState.mat'; % Load intial state in V_init
%% Adjust Network connectivity for Knockout 
if knockedOut == 0 % no neuron is knockedout
    W_syn = W_SYN;
    W_gap = W_GAP;
else % delete the neurons from the graph that are to be knocked out
    % Removing corresponding row and column for adjacency matrix for 
    % Synapse
    W_syn = W_SYN(~ismember(1:9,knockedOut),:); % deleting row first
    W_syn = W_syn(:,~ismember(1:9,knockedOut)); % deleting column 
    
    % Gap-junction
    W_gap = W_GAP(~ismember(1:9,knockedOut),:); % deleting row first
    W_gap = W_gap(:,~ismember(1:9,knockedOut)); % deleting column 
    
    % Deleting other Parameters 
    Cap = Cap(~ismember(1:9,knockedOut));
    Res = Res(~ismember(1:9,knockedOut));
    E_syn = E_syn(~ismember(1:9,knockedOut));
    V_init = V_init(~ismember(1:9,knockedOut));
end

%% Computing Equillibrium potential of each neurons
% Parameter
% Leakage voltage
V_leak = -0.035;
% Gap-junction parameter
g_gap = 5e-9;
%Synaptic Parameters
g_syn = 6e-10; 
N = size(W_syn,1); % Number of Neuron in TW circuit after knockout
% Construct Matrix A
A = zeros(N,N);
B = zeros(N,1);
for i=1:N
    for j=1:N
        if i~=j
            A(i,j) = -Res(i)*W_gap(i,j)*g_gap;
        else
            A(i,j) = 1+Res(i)*sum(W_gap(i,:)*g_gap+0.5*W_syn(i,:)*g_syn);
        end
    end
    B(i) = V_leak+Res(i)*sum(W_syn(i,:)*E_syn*g_syn*0.5);
end
V_eq = linsolve(A,B);

%% Simulation of TW circuit 
simdur = 0.06; % (60 mS)[-0.0280794, -0.0280874, -0.0337083, -0.0280171, -0.0272915, -0.0337002, -0.0161361, -0.0091623, -0.0239873]
dt = 0.00005;   
pulse_stim = 5e-10; % Stimulation strength
startTime = 0.01; % time when stimulation is started  
pulse_dur = 0.03; % stimulation duration

% Constructing Stimulus Input
simStep = int16(simdur/dt);
IStim = zeros(N,simStep+1);
startInd = startTime/dt; endInd = (startTime+pulse_dur)/dt;
IStim(stimID,startInd:endInd) = pulse_stim;

%% Call to Simulation method (ODE45 method)
[store_t,store_V] = ode45('TWModel_dynamics', 0:dt:simdur, V_init);
disp(store_t);
disp(store_V);

initial_size = 1e-4;
T = store_t;
Reach_Dia = zeros(size(T));
Reach_Dia(1) = initial_size;  %set of the initial values
step = 13;
for j = 1:step:length(T)-1
    [V,D] = eig(mainJacobian(mean(store_V(j:min(j+step-1,length(T)),:))));
    for i = j:min(j+step-1,size(T)-1)
        %center = (store_V(i,:));
        center = (store_V(i,:)+store_V(i+1,:))/2;
        Jacobian = mainJacobian(store_V(i,:));
        D = V\Jacobian*V;
        lambda = max(eig((D+D')/2));
        Diff = diffJacobian(mainJacobian(center-initial_size/2),mainJacobian(center+initial_size/2),...
            center-initial_size/2,center+initial_size/2);
        delta = norm(V\((Diff+Diff')/2)*V);
        change_rate = lambda+delta; 
        %disp(lambda);
        Reach_Dia(i+1) = Reach_Dia(i)*exp(change_rate*(T(i+1)-T(i)));
    end
    Reach_Dia(j:min(j+step-1,length(T)),:) = Reach_Dia(j:min(j+step-1,length(T)),:)*cond(V);
end
plot(Reach_Dia);
