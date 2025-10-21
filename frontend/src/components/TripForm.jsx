import React, { useState } from 'react';
import { MapPin, Package, Navigation, Clock, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const TripForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    current_location: '',
    pickup_location: '',
    dropoff_location: '',
    current_cycle_used: '0'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="w-full shadow-xl border-2 border-blue-100 hover:border-blue-200 transition-all duration-300">
      <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50">
        <CardTitle className="flex items-center gap-2 text-xl">
          <div className="p-2 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg">
            <Navigation className="h-5 w-5 text-white" />
          </div>
          Trip Details
        </CardTitle>
        <CardDescription className="text-gray-600">
          Enter your trip information to calculate route and ELD compliance
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="current_location" className="flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              Current Location
            </Label>
            <Input
              id="current_location"
              name="current_location"
              placeholder="e.g., Los Angeles, CA"
              value={formData.current_location}
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="pickup_location" className="flex items-center gap-2">
              <Package className="h-4 w-4" />
              Pickup Location
            </Label>
            <Input
              id="pickup_location"
              name="pickup_location"
              placeholder="e.g., Phoenix, AZ"
              value={formData.pickup_location}
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="dropoff_location" className="flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              Dropoff Location
            </Label>
            <Input
              id="dropoff_location"
              name="dropoff_location"
              placeholder="e.g., Dallas, TX"
              value={formData.dropoff_location}
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="current_cycle_used" className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              Current Cycle Hours Used (70hr/8day)
            </Label>
            <Input
              id="current_cycle_used"
              name="current_cycle_used"
              type="number"
              min="0"
              max="70"
              step="0.5"
              placeholder="0"
              value={formData.current_cycle_used}
              onChange={handleChange}
              required
            />
            <p className="text-xs text-muted-foreground">
              Enter hours already used in your current 8-day cycle (0-70)
            </p>
          </div>

          <Button 
            type="submit" 
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-6 text-lg shadow-lg hover:shadow-xl transition-all duration-300" 
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Calculating Trip...
              </>
            ) : (
              <>
                <Navigation className="mr-2 h-5 w-5" />
                Calculate Trip
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default TripForm;
