import React, { useState } from 'react';
import axios from 'axios';
import { Truck, AlertCircle, Sparkles } from 'lucide-react';
import TripForm from './components/TripForm';
import RouteMap from './components/RouteMap';
import TripSummary from './components/TripSummary';
import ELDLogViewer from './components/ELDLogViewer';
import LoadingModal from './components/LoadingModal';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [error, setError] = useState(null);
  const [tripData, setTripData] = useState(null);

  const handleTripCalculation = async (formData) => {
    setLoading(true);
    setLoadingStep(0);
    setError(null);
    
    try {
      // Simulate progress steps
      setLoadingStep(1); // Geocoding
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setLoadingStep(2); // Calculating route
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setLoadingStep(3); // HOS regulations
      const response = await axios.post(`${API_BASE_URL}/calculate-trip/`, {
        current_location: formData.current_location,
        pickup_location: formData.pickup_location,
        dropoff_location: formData.dropoff_location,
        current_cycle_used: parseFloat(formData.current_cycle_used)
      });

      setLoadingStep(4); // Generating logs
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setTripData(response.data);
    } catch (err) {
      console.error('Error calculating trip:', err);
      setError(
        err.response?.data?.error || 
        'Failed to calculate trip. Please check your inputs and try again.'
      );
    } finally {
      setLoading(false);
      setLoadingStep(0);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Loading Modal */}
      <LoadingModal isOpen={loading} currentStep={loadingStep} />
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-200 sticky top-0 z-40">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl shadow-lg">
                <Truck className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  ELD Trip Planner
                </h1>
                <p className="text-sm text-gray-600 flex items-center gap-1">
                  <Sparkles className="h-3 w-3" />
                  Smart route planning with HOS compliance
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Form */}
          <div className="lg:col-span-1">
            <TripForm onSubmit={handleTripCalculation} loading={loading} />
            
            {/* Error Display */}
            {error && (
              <Card className="mt-4 border-red-200 bg-red-50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-red-700">
                    <AlertCircle className="h-5 w-5" />
                    Error
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-red-700">{error}</p>
                </CardContent>
              </Card>
            )}

            {/* Info Card */}
            {!tripData && !error && (
              <Card className="mt-4 border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-blue-600" />
                    How It Works
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm space-y-2">
                  <p>
                    <strong>1.</strong> Enter your current location, pickup, and dropoff addresses
                  </p>
                  <p>
                    <strong>2.</strong> Specify hours already used in your 70hr/8-day cycle
                  </p>
                  <p>
                    <strong>3.</strong> Get a complete route with:
                  </p>
                  <ul className="list-disc list-inside ml-4 space-y-1 text-muted-foreground">
                    <li>Turn-by-turn directions</li>
                    <li>Required rest breaks (10hr minimum)</li>
                    <li>Fuel stops (every 1000 miles)</li>
                    <li>ELD logs for each day</li>
                    <li>HOS compliance verification</li>
                  </ul>
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-xs text-blue-900">
                      <strong>Note:</strong> Calculations assume 70hr/8-day cycle for property-carrying drivers,
                      55mph average speed, and 1-hour for pickup/dropoff.
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            {tripData ? (
              <>
                {/* Tabs for different views */}
                <Tabs defaultValue="map" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="map">Map & Route</TabsTrigger>
                    <TabsTrigger value="summary">Trip Summary</TabsTrigger>
                    <TabsTrigger value="logs">ELD Logs</TabsTrigger>
                  </TabsList>

                  <TabsContent value="map" className="space-y-4">
                    <Card>
                      <CardHeader>
                        <CardTitle>Route Map</CardTitle>
                        <CardDescription>
                          Your route from {tripData.route.current_location.address} to{' '}
                          {tripData.route.dropoff_location.address}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <RouteMap routeData={tripData.route} />
                      </CardContent>
                    </Card>

                    {/* Quick Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <Card>
                        <CardHeader className="pb-3">
                          <CardDescription>Distance</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <p className="text-2xl font-bold">
                            {tripData.summary.total_distance_miles.toFixed(0)} mi
                          </p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardHeader className="pb-3">
                          <CardDescription>Duration</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <p className="text-2xl font-bold">
                            {Math.round(tripData.summary.estimated_duration_hours)}h
                          </p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardHeader className="pb-3">
                          <CardDescription>Rest Stops</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <p className="text-2xl font-bold">
                            {tripData.summary.num_rest_breaks}
                          </p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardHeader className="pb-3">
                          <CardDescription>Days</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <p className="text-2xl font-bold">
                            {tripData.summary.num_days}
                          </p>
                        </CardContent>
                      </Card>
                    </div>
                  </TabsContent>

                  <TabsContent value="summary">
                    <TripSummary 
                      summary={tripData.summary} 
                      tripPlan={tripData.trip_plan}
                    />
                  </TabsContent>

                  <TabsContent value="logs">
                    <ELDLogViewer 
                      logSheets={tripData.log_sheets}
                      dailyLogs={tripData.trip_plan.daily_logs}
                    />
                  </TabsContent>
                </Tabs>
              </>
            ) : (
              <Card className="h-[600px] flex items-center justify-center">
                <CardContent className="text-center">
                  <Truck className="h-24 w-24 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Ready to Plan Your Trip?</h3>
                  <p className="text-muted-foreground">
                    Enter your trip details to get started
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 bg-white border-t">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            ELD Trip Planner - Compliant with FMCSA Hours of Service regulations
          </p>
          <p className="mt-1">
            For educational and planning purposes. Always verify with official sources.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
