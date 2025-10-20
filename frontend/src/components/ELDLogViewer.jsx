import React, { useState } from 'react';
import { FileText, Download, ChevronLeft, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

const ELDLogViewer = ({ logSheets, dailyLogs }) => {
  const [currentLogIndex, setCurrentLogIndex] = useState(0);

  if (!logSheets || logSheets.length === 0) {
    return null;
  }

  const currentLog = dailyLogs[currentLogIndex];
  const currentSheet = logSheets[currentLogIndex];

  const handlePrevious = () => {
    setCurrentLogIndex(prev => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    setCurrentLogIndex(prev => Math.min(logSheets.length - 1, prev + 1));
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${currentSheet}`;
    link.download = `eld-log-${currentLog.date}.png`;
    link.click();
  };

  const formatHours = (hours) => {
    return hours.toFixed(1);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-primary" />
              Daily ELD Logs
            </CardTitle>
            <CardDescription>
              Log {currentLogIndex + 1} of {logSheets.length} - {new Date(currentLog.date).toLocaleDateString()}
            </CardDescription>
          </div>
          <Button onClick={handleDownload} variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Download
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {/* Log Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-xs text-muted-foreground">Driving Hours</p>
            <p className="text-xl font-bold text-blue-600">
              {formatHours(currentLog.driving_hours)}h
            </p>
          </div>
          <div className="bg-green-50 p-3 rounded-lg">
            <p className="text-xs text-muted-foreground">On Duty Hours</p>
            <p className="text-xl font-bold text-green-600">
              {formatHours(currentLog.on_duty_hours)}h
            </p>
          </div>
          <div className="bg-purple-50 p-3 rounded-lg">
            <p className="text-xs text-muted-foreground">Off Duty Hours</p>
            <p className="text-xl font-bold text-purple-600">
              {formatHours(currentLog.off_duty_hours)}h
            </p>
          </div>
          <div className="bg-orange-50 p-3 rounded-lg">
            <p className="text-xs text-muted-foreground">Total Miles</p>
            <p className="text-xl font-bold text-orange-600">
              {currentLog.total_miles.toFixed(1)}
            </p>
          </div>
        </div>

        {/* Log Sheet Image */}
        <div className="border rounded-lg overflow-hidden bg-white">
          <img
            src={`data:image/png;base64,${currentSheet}`}
            alt={`ELD Log for ${currentLog.date}`}
            className="w-full h-auto"
          />
        </div>

        {/* Navigation */}
        {logSheets.length > 1 && (
          <div className="flex justify-between items-center mt-4">
            <Button
              onClick={handlePrevious}
              disabled={currentLogIndex === 0}
              variant="outline"
            >
              <ChevronLeft className="h-4 w-4 mr-2" />
              Previous Day
            </Button>
            <span className="text-sm text-muted-foreground">
              Day {currentLogIndex + 1} of {logSheets.length}
            </span>
            <Button
              onClick={handleNext}
              disabled={currentLogIndex === logSheets.length - 1}
              variant="outline"
            >
              Next Day
              <ChevronRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        )}

        {/* Timeline Details */}
        <div className="mt-6">
          <h4 className="font-semibold mb-3">Activity Timeline</h4>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {currentLog.timeline.map((entry, index) => (
              <div
                key={index}
                className="flex justify-between items-center p-2 bg-muted rounded text-sm"
              >
                <div>
                  <span className="font-medium">{entry.activity}</span>
                  <span className="text-muted-foreground ml-2">
                    {new Date(entry.start_time).toLocaleTimeString()}
                  </span>
                </div>
                <div className="text-right">
                  <span className="font-medium">
                    {entry.duration.toFixed(1)}h
                  </span>
                  {entry.distance > 0 && (
                    <span className="text-muted-foreground ml-2">
                      {entry.distance.toFixed(1)} mi
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ELDLogViewer;
