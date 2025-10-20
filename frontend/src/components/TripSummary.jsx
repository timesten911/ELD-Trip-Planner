import React from 'react';
import { Clock, MapPin, Coffee, Moon, Calendar, Gauge } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const TripSummary = ({ summary, tripPlan }) => {
  if (!summary) return null;

  const formatHours = (hours) => {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    return `${h}h ${m}m`;
  };

  const stats = [
    {
      icon: MapPin,
      label: 'Total Distance',
      value: `${summary.total_distance_miles.toFixed(1)} miles`,
      color: 'text-blue-600'
    },
    {
      icon: Clock,
      label: 'Estimated Duration',
      value: formatHours(summary.estimated_duration_hours),
      color: 'text-green-600'
    },
    {
      icon: Moon,
      label: 'Rest Breaks',
      value: summary.num_rest_breaks,
      color: 'text-purple-600'
    },
    {
      icon: Coffee,
      label: 'Fuel Stops',
      value: summary.num_fuel_stops,
      color: 'text-orange-600'
    },
    {
      icon: Calendar,
      label: 'Trip Days',
      value: summary.num_days,
      color: 'text-indigo-600'
    },
    {
      icon: Gauge,
      label: 'Cycle Hours Remaining',
      value: `${summary.cycle_hours_remaining.toFixed(1)}h`,
      color: 'text-red-600'
    }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Trip Summary</CardTitle>
        <CardDescription>Overview of your planned trip</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {stats.map((stat, index) => (
            <div key={index} className="flex flex-col space-y-2 p-4 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <stat.icon className={`h-5 w-5 ${stat.color}`} />
                <span className="text-sm text-muted-foreground">{stat.label}</span>
              </div>
              <span className="text-2xl font-bold">{stat.value}</span>
            </div>
          ))}
        </div>

        {tripPlan && tripPlan.segments && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">Trip Segments</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {tripPlan.segments.map((segment, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg border ${
                    segment.type === 'driving'
                      ? 'bg-blue-50 border-blue-200'
                      : segment.type === 'rest'
                      ? 'bg-purple-50 border-purple-200'
                      : 'bg-green-50 border-green-200'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium">{segment.activity}</p>
                      <p className="text-sm text-muted-foreground">
                        {new Date(segment.start_time).toLocaleString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">
                        {formatHours(segment.duration)}
                      </p>
                      {segment.distance > 0 && (
                        <p className="text-xs text-muted-foreground">
                          {segment.distance.toFixed(1)} mi
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default TripSummary;
