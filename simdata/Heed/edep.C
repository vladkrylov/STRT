#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <utility>

#include <TCanvas.h>
#include <TROOT.h>
#include <TApplication.h>
#include <TH1F.h>
#include <TMath.h>
#include <TRandom3.h>

#include "MediumMagboltz.hh"
#include "SolidBox.hh"
#include "GeometrySimple.hh"
#include "ComponentConstant.hh"
#include "Sensor.hh"
#include "TrackHeed.hh"
#include "Plotting.hh"

using namespace Garfield;

template <typename T> T StringToNumber ( const std::string &Text );
int ParseArguments(int argc, char * argv[],
		           double& d0Mean,
				   double& d0Sigma,
				   double& phiMean,
				   double& phiSigma,
				   int& nEvents,
				   double& meanNTracksPerEvent);
int Diffuse(std::vector<double>& x0, std::vector<double>& y0, double sigma, double initDirection);
int WriteEventYAML(std::ofstream& outfile, int eventId, const std::vector<double>& xEventHits, const std::vector<double>& yEventHits);
int WriteTrackYAML(std::ofstream& outfile, int trackId, int eventId, double xline[2], double yline[2], const std::vector<int>& hitIndices);
bool HitsSortFunction(std::pair<double, double> h1, std::pair<double, double> h2) { return (h1.first < h2.first); }

int main(int argc, char * argv[])
{
  double d0Mean = 0.;
  double d0Sigma = 0.;
  double phiMean = 0.;
  double phiSigma = 0.;
  int nEvents = 0;
  double meanNTracksPerEvent = 0.;
  if (ParseArguments(argc, argv, d0Mean, d0Sigma, phiMean, phiSigma, nEvents, meanNTracksPerEvent) != 0)
	return 0;

  // output data structures
  std::vector<double> xEventHits;
  std::vector<double> yEventHits;
  std::vector<double> xTrackHits;
  std::vector<double> yTrackHits;
  std::vector<int> hit_indices;
  double xline[2], yline[2];
  ofstream tracksYAML;
  ofstream eventsYAML;
  tracksYAML.open("tracks.yaml");
  eventsYAML.open("events.yaml");

  TApplication app("app", &argc, argv);
  plottingEngine.SetDefaultStyle();

  // Histograms
  TH1::StatOverflows(kTRUE);
  TH1F* hElectrons = new TH1F("hElectrons", "Number of electrons",
                              200, 0, 200);
  TH1F* hEdep = new TH1F("hEdep", "Energy Loss",
                         100, 0., 10.);

  // Make a medium
  MediumMagboltz* gas = new MediumMagboltz();
  gas->SetComposition("he", 80., "isobutane", 20.);
  gas->SetTemperature(293.15);
  gas->SetPressure(760.);

  // Detector geometry
  // Gap [cm]
  const double x = 63.32;
  const double y = 80.32;
  const double z = 2.;
  const double xc = x/2.;
  const double yc = 80.32;
  SolidBox* box = new SolidBox(xc, yc, 0., x/2., y/2., z/2.);
  GeometrySimple* geo = new GeometrySimple();
  geo->AddSolid(box, gas);

  // Make a component
  ComponentConstant* comp = new ComponentConstant();
  comp->SetGeometry(geo);
  comp->SetElectricField(0., 0., 0.);

  // Make a sensor
  Sensor* sensor = new Sensor();
  sensor->AddComponent(comp);

  // Track class
  TrackHeed* track = new TrackHeed();
  track->SetSensor(sensor);
  track->SetParticle("e-");
  track->SetEnergy(1.69e6);

  track->EnableDebugging();
  TRandom3 r;
  for (int i = 0; i < nEvents; ++i) {
    if (i == 1) track->DisableDebugging();
    if (i % 1000 == 0) std::cout << i << "/" << nEvents << "\n";

    xEventHits.clear();
    yEventHits.clear();
    int nTracks = r.Poisson(meanNTracksPerEvent);

    for (int j = 0; j < nTracks; j++) {
	  // Initial position and direction
	  double x0 = 0;
	  double y0 = r.Gaus(d0Mean, d0Sigma);
	  double z0 = 0., t0 = 0.;
	  double phi = r.Gaus(phiMean, phiSigma);
	  double dx0 = TMath::Cos(phi);
	  double dy0 = TMath::Sin(phi);
	  double dz0 = 0.;
	  track->NewTrack(x0, y0, z0, t0, dx0, dy0, dz0);
	  xTrackHits.clear();
	  yTrackHits.clear();

	  // Cluster coordinates
	  double xc = 0., yc = 0., zc = 0., tc = 0.;
	  // Number of electrons produced in a collision
	  int nc = 0;
	  // Energy loss in a collision
	  double ec = 0.;
	  // Dummy variable (not used at present)
	  double extra = 0.;
	  // Total energy loss along the track
	  double esum = 0.;
	  // Total number of electrons produced along the track
	  int nsum = 0;
	  // Loop over the clusters.
	  while (track->GetCluster(xc, yc, zc, tc, nc, ec, extra)) {
	    esum += ec;
	    nsum += nc;
	    xTrackHits.push_back(xc);
	    yTrackHits.push_back(yc);
	  }
	  // sorting
	  std::vector< std::pair<double, double> > hits;
	  for(int ih=0; ih<xTrackHits.size(); ih++) {
		  hits.push_back(std::pair<double, double>(xTrackHits.at(ih), yTrackHits.at(ih)));
	  }
	  std::sort (hits.begin(), hits.end(), HitsSortFunction);
	  for(int ih=0; ih<xTrackHits.size(); ih++) {
		  xTrackHits[ih] = hits[ih].first;
		  yTrackHits[ih] = hits[ih].second;
	  }
	  // Diffusion
	  Diffuse(xTrackHits, yTrackHits, 0.09, phi);
	  // Fill track info
	  hit_indices.clear();
	  int startInd = xEventHits.size();
	  xEventHits.insert(xEventHits.end(), xTrackHits.begin(), xTrackHits.end());
	  yEventHits.insert(yEventHits.end(), yTrackHits.begin(), yTrackHits.end());
	  for(int ih=startInd; ih<xEventHits.size(); ih++) {
		  hit_indices.push_back(ih);
	  }
	  xline[0] = xEventHits[hit_indices.at(0)];
	  xline[1] = xEventHits[hit_indices.at(hit_indices.size()-1)];
	  yline[0] = yEventHits[hit_indices.at(0)];
	  yline[1] = yEventHits[hit_indices.at(hit_indices.size()-1)];
	  WriteTrackYAML(tracksYAML, j, i, xline, yline, hit_indices);

	  hElectrons->Fill(nsum);
	  hEdep->Fill(esum * 1.e-3);
    }
    WriteEventYAML(eventsYAML, i, xEventHits, yEventHits);
  }

  eventsYAML.close();

//  app.Run(kTRUE);

}

int ParseArguments(int argc, char * argv[],
				   double& d0Mean,
				   double& d0Sigma,
				   double& phiMean,
				   double& phiSigma,
				   int& nEvents,
				   double& meanNTracksPerEvent)
{
  if (argc < 7) {
    std::cout <<"Input parameters needs to be set in format:"<< std::endl;
	std::cout << "D0_min D0_max phi_min phi_max n_events mean_ntracks_per_event" << std::endl;
	return 0;
  }
  d0Mean = StringToNumber<double>(argv[1]);
  d0Sigma = StringToNumber<double>(argv[2]);
  phiMean = StringToNumber<double>(argv[3]);
  phiSigma = StringToNumber<double>(argv[4]);
  nEvents = StringToNumber<int>(argv[5]);
  meanNTracksPerEvent = StringToNumber<double>(argv[6]);
  return 0;
}

template <typename T>
T StringToNumber ( const std::string &Text )//Text not by const reference so that the function can be used with a
{                               //character array as argument
	std::stringstream ss(Text);
	T result;
	return ss >> result ? result : 0;
}

int Diffuse(std::vector<double>& x0, std::vector<double>& y0, double sigma, double initDirection)
{
	TRandom3 r;
	for(size_t i=0; i<x0.size(); i++) {
		double d = r.Gaus(0., sigma);
		x0[i] -= d*TMath::Sin(initDirection);
		y0[i] += d*TMath::Cos(initDirection);
	}
	return 0;
}

int WriteEventYAML(std::ofstream& outfile, int eventId, const std::vector<double>& xEventHits, const std::vector<double>& yEventHits)
{
	outfile << "# New Event" << std::endl;
	outfile << "id: " << eventId << std::endl;
	if (xEventHits.size() == 0) {
		outfile << "xhits: []" << std::endl;
	} else {
		outfile << "xhits: [" << xEventHits[0];
		for(size_t i=1; i<xEventHits.size(); i++) {
			outfile << ", " << xEventHits[i];
		}
		outfile << "]"  << std::endl;
	}


	if (yEventHits.size() == 0) {
		outfile << "yhits: []" << std::endl;
	} else {
		outfile << "yhits: [" << yEventHits[0];
		for(size_t i=1; i<yEventHits.size(); i++) {
			outfile << ", " << yEventHits[i];
		}
		outfile << "]"  << std::endl;
	}
	return 0;
}

int WriteTrackYAML(std::ofstream& outfile, int trackId, int eventId, double xline[2], double yline[2], const std::vector<int>& hitIndices)
{
	outfile << "!!python/object:model.global_coords.data_structures.Track" << std::endl;
	outfile << "id: " << trackId << std::endl;
	outfile << "event_id: " << eventId << std::endl;
	if (hitIndices.size() == 0) {
		outfile << "hit_indices: []" << std::endl;
	} else {
		outfile << "hit_indices: [" << hitIndices[0];
		for(size_t i=1; i<hitIndices.size(); i++) {
			outfile << ", " << hitIndices[i];
		}
		outfile << "]"  << std::endl;

		outfile << "line: !!python/tuple" << std::endl;
		outfile << "- [" << xline[0] << ", " << xline[1] << "]" << std::endl;
		outfile << "- [" << yline[0] << ", " << yline[1] << "]" << std::endl;
		outfile << "---" << std::endl;
	}
	return 0;
}

