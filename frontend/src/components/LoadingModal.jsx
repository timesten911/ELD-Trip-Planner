import React from 'react';
import { Loader2, MapPin, Route, FileText } from 'lucide-react';

const LoadingModal = ({ isOpen, currentStep }) => {
  if (!isOpen) return null;

  const steps = [
    { id: 1, label: 'Geocoding locations', icon: MapPin, color: 'text-blue-500' },
    { id: 2, label: 'Calculating optimal route', icon: Route, color: 'text-green-500' },
    { id: 3, label: 'Applying HOS regulations', icon: FileText, color: 'text-purple-500' },
    { id: 4, label: 'Generating ELD logs', icon: FileText, color: 'text-orange-500' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4 animate-in fade-in zoom-in duration-300">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full mb-4">
            <Loader2 className="w-8 h-8 text-white animate-spin" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            Calculating Your Trip
          </h3>
          <p className="text-gray-600">
            Please wait while we plan your route...
          </p>
        </div>

        {/* Progress Steps */}
        <div className="space-y-4">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = currentStep >= step.id;
            const isComplete = currentStep > step.id;
            
            return (
              <div
                key={step.id}
                className={`flex items-center gap-4 p-4 rounded-xl transition-all duration-500 ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200'
                    : 'bg-gray-50 border-2 border-transparent'
                }`}
              >
                <div
                  className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500 ${
                    isComplete
                      ? 'bg-green-500'
                      : isActive
                      ? 'bg-gradient-to-br from-blue-500 to-indigo-600'
                      : 'bg-gray-300'
                  }`}
                >
                  {isComplete ? (
                    <svg
                      className="w-6 h-6 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={3}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  ) : (
                    <Icon
                      className={`w-5 h-5 ${
                        isActive ? 'text-white' : 'text-gray-500'
                      } ${isActive && !isComplete ? 'animate-pulse' : ''}`}
                    />
                  )}
                </div>
                <div className="flex-1">
                  <p
                    className={`font-semibold transition-colors duration-300 ${
                      isActive ? 'text-gray-900' : 'text-gray-500'
                    }`}
                  >
                    {step.label}
                  </p>
                </div>
                {isActive && !isComplete && (
                  <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
                )}
              </div>
            );
          })}
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500 ease-out"
              style={{ width: `${(currentStep / steps.length) * 100}%` }}
            />
          </div>
          <p className="text-center text-sm text-gray-600 mt-2">
            Step {currentStep} of {steps.length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoadingModal;
