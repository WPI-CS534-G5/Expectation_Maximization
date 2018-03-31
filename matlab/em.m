% Function em:
% Input params: p1 -> name of the file with the data
%               p2 -> number of clusters
function exitcode=em2(p1,p2)
    msg=sprintf('Simulation started at %s *********\n',datestr(clock));
    disp(msg);

    %Load data and define the number of clusters     
        file_name=p1;
        if(~exist(file_name,'file'))
            msg=sprintf('Error! File "%s" does not exist in the current directory!',file_name);
            disp(msg)
            exit;
        end
        data=csvread(file_name);
        lData=size(data,1);
        dataDim=size(data,2);
        
        if(p2=='X'|p2=='x')
            nFlag=0;
            iniCluster=1;
            endCluster=lData;
        else
            nFlag=1;
            NroClusters=str2num(p2);  %Because p2 is type string
            iniCluster=NroClusters;
            endCluster=NroClusters;
        end
        
        max_error=0.00001;  %Max difference in the likely hood function before to stop the simulation
        bestLLG=-inf;   
 for(NroClusters=iniCluster:endCluster)
    % Initialize variables
        cMeans=[];  %Means vector. (Centers of the clusters)
        cStd=cell(1,NroClusters);   %Standar deviation cell. Each value is a correlation matriz of size [2x2]/
                                    % This size depende the dimensions of the data
        Pc=(1/NroClusters).*ones(1,NroClusters);  % Vector which contain the probabilities of each cluster. Phi vector.
                                                  % At the beginning we set the probabilities all the same.
   
    msg=sprintf('Testing centers for model with %d clusters:',NroClusters);
    disp(msg)
    for(modelTest=1:10)   
        %1. Initial values: We choose two points randomly.
            A=cov(data)/NroClusters;
            for(i=1:NroClusters)
                for(k=1:dataDim)
                    nro=round(rand(1)*(lData-1))+1;
                    cMeans(i,k)=data(nro,k);     %We get the means for each cluster randomly. 
                end
                cStd{i}=A;
            end
        for(iter=1:100)

        %2. Expectation   
            cPdf=zeros(lData,NroClusters);   %Contain the probabilities of the each distribution (size of data x 3clusters).
                                             %It is useful later to calculate the maximun likelihood
            z=zeros(lData,NroClusters);      %Same that the previous, but now it will contain the the previos value x Phi vector
            for(i=1:NroClusters)
               cPdf(:,i)=mvnpdf(data,cMeans(i,:),cStd{i});  %This function is the multivariate gaussian distributions.
               z(:,i)=cPdf(:,i).*Pc(1,i);
            end
            %Normalization
            zSum=sum(z,2);
            zFind=find(zSum==0);  %If we get a zero in the denominator, we leave that values or means and sigmas
            if(~isempty(zFind))
                break;
            end
            for(i=1:NroClusters)
                z(:,i)=z(:,i)./zSum;
            end

        % 3. Maximization
            Pc=mean(z);
            deno=sum(z);
            cMeans=(data'*z)';
            for(i=1:NroClusters)
                cMeans(i,:)=cMeans(i,:)./deno(i);  %Update means
                mData=bsxfun(@minus,data,cMeans(i,:));  % function is only to substract a vector (cMeans) from a matrix (data)
                mDataT(:,1)=mData(:,1).*z(:,i);
                mDataT(:,2)=mData(:,2).*z(:,i);
                sigma=mDataT'*mData./deno(i);      
                cStd{i}=sigma;  % Update sigmas
            end
            llg(iter)=sum(log(cPdf*Pc'));   %Maximum Likelihood calculation
            %msg=sprintf('Itera:%d Log(P):%f',iter,llg(iter));
            %disp(msg)
            if(iter>1)
                error=llg(iter)-llg(iter-1);
                if(error<0.00001)
                    break;
                end
            end
        end
        CurrentLLG=llg(iter);
        BIC(NroClusters)=-2*llg(iter)+NroClusters*5*log(lData);
        msg=sprintf('     NroClusters:%d BIC=%.4f Log(L):%.4f',NroClusters,BIC(NroClusters),llg(iter));
        disp(msg)
        
        %We save the better cluster
        if(CurrentLLG>bestLLG) 
            fBIC(NroClusters)=BIC(NroClusters);
            bestLLG(NroClusters)=CurrentLLG;
            fCenters{NroClusters}=cMeans;
            fCovariance{NroClusters}=cStd; 
        end        
    end
    if(NroClusters>1&nFlag==0)
            if(BIC(NroClusters-1)-BIC(NroClusters)<0)
                break;
            end
    end 
 end
    if(nFlag==0)
        NroClusters=NroClusters-1;
    end
    fCenter_=fCenters{NroClusters};
    fCovariance_=fCovariance{NroClusters};
    % Reporting results ***************************
            msg=sprintf('\nEnd of simulation at %s********************************\n',datestr(clock));
            disp(msg)
            msg=sprintf('NroClusters:%d BIC=%f Log(L):%f',NroClusters,fBIC(NroClusters),bestLLG(NroClusters));
            disp(msg)
            msg=sprintf('Dimensionality of data:%d\n',dataDim);
            disp(msg)
            msg=sprintf('~ Best Clusters: ~\n');
            disp(msg)
            for(i=1:NroClusters)
            msg=sprintf('|----Cluster %d--------------------------|',i);
            disp(msg)
                msg=sprintf('Center:[X1  X2 ...... Xn]');
                disp(msg)
                display(fCenter_(i,:))
                msg=sprintf('Covariance Matrix:');
                disp(msg)
                fCovariance_{i}
            end
    %**********************************
    
    exitcode=0;
end
                                       

    