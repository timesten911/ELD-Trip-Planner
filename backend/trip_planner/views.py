"""
API Views for Trip Planner
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .eld_service import ELDService
from .routing_service import RoutingService
from .log_generator import ELDLogGenerator
from datetime import datetime


@api_view(['POST'])
def calculate_trip(request):
    """
    Calculate trip with route and ELD compliance
    
    Expected input:
    {
        "current_location": "Address or coordinates",
        "pickup_location": "Address or coordinates",
        "dropoff_location": "Address or coordinates",
        "current_cycle_used": 25.5
    }
    """
    try:
        # Extract input data
        current_location = request.data.get('current_location')
        pickup_location = request.data.get('pickup_location')
        dropoff_location = request.data.get('dropoff_location')
        current_cycle_used = float(request.data.get('current_cycle_used', 0))
        
        # Validate inputs
        if not all([current_location, pickup_location, dropoff_location]):
            return Response(
                {'error': 'Missing required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize services
        routing_service = RoutingService()
        eld_service = ELDService(current_cycle_used)
        log_generator = ELDLogGenerator()
        
        # Calculate route
        route_data = routing_service.get_route_with_stops(
            current_location,
            pickup_location,
            dropoff_location
        )
        
        # Calculate ELD compliance and trip plan
        trip_plan = eld_service.calculate_trip_plan(
            route_data['total_distance_miles'],
            datetime.now()
        )
        
        # Generate log sheets with trip details
        trip_details = {
            'driver_name': "Driver",
            'from_location': current_location,
            'to_location': dropoff_location,
            'carrier_name': "Transport Company",
            'main_office': "123 Main St, City, State",
            'home_terminal': current_location,
            'truck_number': "TRK-001",
            'trailer_number': "TRL-001"
        }
        log_sheets = log_generator.generate_all_logs(
            trip_plan['daily_logs'],
            trip_details
        )
        
        # Combine all data
        response_data = {
            'route': route_data,
            'trip_plan': trip_plan,
            'log_sheets': log_sheets,
            'summary': {
                'total_distance_miles': route_data['total_distance_miles'],
                'estimated_duration_hours': trip_plan['estimated_duration_hours'],
                'num_rest_breaks': trip_plan['num_rest_breaks'],
                'num_fuel_stops': trip_plan['num_fuel_stops'],
                'num_days': len(trip_plan['daily_logs']),
                'cycle_hours_remaining': trip_plan['cycle_hours_available']
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response(
            {'error': f'Invalid input: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error in calculate_trip: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {'error': f'Server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def geocode(request):
    """
    Geocode an address to coordinates
    
    Expected input:
    {
        "address": "123 Main St, City, State"
    }
    """
    try:
        address = request.data.get('address')
        
        if not address:
            return Response(
                {'error': 'Address is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        routing_service = RoutingService()
        coords = routing_service.geocode_address(address)
        
        return Response({
            'address': address,
            'latitude': coords[0],
            'longitude': coords[1]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Geocoding error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }, status=status.HTTP_200_OK)
