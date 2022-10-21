% 0 to turn off, 1 to turn on plotting these things
PLOT_ACC = 0;
PLOT_ACC_FILT = 1;
PLOT_FPR = 0;

% Restrict graph to certain time (in seconds). Use -inf and inf if 
% you don't want to restrict.
time_limits = [5, 10];

% close all open graphs
close all;

% tell matlab to plot multiple things on the same graph if necessary
hold on;
xlabel("Time (seconds)");
xlim(time_limits);

% Open a window for the user to select the folder
folder = uigetdir("Select DAQ folder");
% Get a list of all .csv in the folder
csv_files=dir(strcat(folder,'\*.csv'));
% Create a file to store their combined data
fileout='merged.txt';
fout=fopen(strcat(folder, "\", fileout),'w');
% Go through all the csv files
for cntfiles=1:length(csv_files)
    % Open the file
    fin=fopen(strcat(folder, "\", csv_files(cntfiles).name));
    % Read the data into temp
    temp = fread(fin,'uint8');
    % put temp into the output file
    fwrite(fout,temp,'uint8');
    % write a new line
    fprintf(fout,'\n');
    % close the csv file
    fclose(fin);
end
% close the combined file
fclose(fout);

% Read the merged file into a table
data = readtable(strcat(folder,"\",fileout));
% get the first column (message names, eg ACC)
data_msg_names = data{:,1};

% 1 where there's an ACC line, 0 where not
acc_lines = strcmp(data_msg_names, "ACC");
% get second column at those lines, which is the time in microseconds
% divide by 1000000 to get seconds
acc_timestamps = data{acc_lines, 2}./1e6;

% check to see that there are at least 3 lines of data
if length(acc_timestamps) > 2

    % average microseconds between samples
    dt = acc_timestamps(2:end) - acc_timestamps(1:end-1);
    avg_dt = sum(dt) / length(dt);
    
    % turn the columns into their own arrays
    accx_data = data{acc_lines, 3};
    accy_data = data{acc_lines, 4};
    accz_data = data{acc_lines, 5};
    accm_data = sqrt(accx_data.^2 + accy_data.^2 + accy_data.^2);
    
    % apply high pass filter at 0.1 Hz
    accx_filt = highpass(accx_data, 0.1, 1/avg_dt);
    accy_filt = highpass(accy_data, 0.1, 1/avg_dt);
    accz_filt = highpass(accz_data, 0.1, 1/avg_dt);
    accm_filt = sqrt(accx_filt.^2 + accy_filt.^2 + accy_filt.^2);

    if PLOT_ACC
        % plot raw acceleration
        plot(acc_timestamps, accx_data);
        plot(acc_timestamps, accy_data);
        plot(acc_timestamps, accz_data);
        plot(acc_timestamps, accm_data);
        legend("X Acc", "Y Acc", "Z Acc", "Magnitude");
        limits

    end

    if PLOT_ACC_FILT
        % Plot filtered acceleration
        plot(acc_timestamps, accx_filt);
        plot(acc_timestamps, accy_filt);
        plot(acc_timestamps, accz_filt);
        plot(acc_timestamps, accm_filt);
        legend("Filtered X Acc.", "Filtered Y Acc.", ...
            "Filtered Z Acc.", "Filtered Acc Magnitude");
    end

else

    disp("No accelerometer data!");

end

can_lines = startsWith(data_msg_names, "CAN");

if sum(can_lines) > 2

    can_data = data{can_lines, :};
    can_ids = can_data(:,4);

    fpr_lines = startsWith(can_ids{:,:}, "01F0A004");
    fpr_data = can_data(fpr_lines,:);
    fpr_timestamps = fpr_data{:,2}./1e6;
    fpr_hex_strings = extractBetween(fpr_data{:,5}, 7, 8);
    fpr_byte = hex2dec(fpr_hex_strings);
    % PSIg
    fpr_values = fpr_byte * 0.580151;
    
    if PLOT_FPR
        plot(fpr_timestamps, fpr_values);
        legend("FPR (PSIg)");
    end

else

    disp("No CAN data!");

end
