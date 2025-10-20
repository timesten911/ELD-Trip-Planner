"""
ELD Compliance Service
Handles Hours of Service (HOS) calculations for property-carrying drivers
Rules: 70 hours/8 days, 11-hour driving limit, 14-hour on-duty limit, 10-hour rest break
"""
from datetime import datetime, timedelta, MINYEAR, MAXYEAR
from typing import List, Dict, Tuple
import math


class ELDService:
    # HOS Rules for property-carrying drivers
    MAX_DRIVING_HOURS = 11  # Maximum driving time per day
    MAX_ON_DUTY_HOURS = 14  # Maximum on-duty time per day
    MIN_REST_HOURS = 10  # Minimum consecutive rest break
    MAX_CYCLE_HOURS = 70  # Maximum hours in 8 days
    CYCLE_DAYS = 8
    
    # Average speeds and times
    AVG_SPEED_MPH = 55  # Average highway speed
    FUEL_STOP_DURATION = 0.5  # 30 minutes for fueling
    FUEL_INTERVAL_MILES = 1000  # Fuel every 1000 miles
    PICKUP_DROPOFF_DURATION = 1.0  # 1 hour for pickup/dropoff
    
    def __init__(self, current_cycle_used: float):
        """
        Initialize ELD service with current cycle hours used
        
        Args:
            current_cycle_used: Hours already used in current 8-day cycle
        """
        self.current_cycle_used = current_cycle_used
        self.available_cycle_hours = self.MAX_CYCLE_HOURS - current_cycle_used
    
    def _safe_add_time(self, dt: datetime, hours: float) -> datetime:
        """Safely add hours to datetime, preventing date overflow"""
        try:
            # Validate input datetime first
            if dt.year < MINYEAR or dt.year > MAXYEAR:
                dt = datetime.now()
            
            # Limit hours to prevent overflow (max 240 hours = 10 days)
            hours = min(abs(hours), 240)
            new_dt = dt + timedelta(hours=hours)
            
            # Validate result is in valid range
            if new_dt.year < MINYEAR or new_dt.year > MAXYEAR:
                # Return original time plus 1 hour as fallback
                return dt + timedelta(hours=1)
            return new_dt
        except (OverflowError, ValueError, AttributeError):
            # If any error, return current time plus small increment
            try:
                return datetime.now() + timedelta(hours=min(hours, 1))
            except:
                return datetime.now()
    
    def calculate_trip_plan(self, distance_miles: float, start_time: datetime = None) -> Dict:
        """
        Calculate complete trip plan with rest stops and ELD compliance
        
        Args:
            distance_miles: Total trip distance in miles
            start_time: Trip start time (defaults to now)
            
        Returns:
            Dictionary containing trip segments, rest stops, and ELD logs
        """
        if start_time is None:
            start_time = datetime.now()
        
        # Validate distance (max 5000 miles to prevent date overflow)
        if distance_miles > 5000:
            raise ValueError("Trip distance exceeds maximum of 5000 miles")
        
        if distance_miles <= 0:
            raise ValueError("Trip distance must be greater than 0")
        
        # Calculate number of fuel stops needed
        num_fuel_stops = math.floor(distance_miles / self.FUEL_INTERVAL_MILES)
        
        # Calculate total driving time (hours)
        base_driving_time = distance_miles / self.AVG_SPEED_MPH
        
        # Add pickup and dropoff time
        total_on_duty_time = base_driving_time + (2 * self.PICKUP_DROPOFF_DURATION)
        
        # Add fuel stop time
        total_on_duty_time += num_fuel_stops * self.FUEL_STOP_DURATION
        
        # Calculate trip segments with rest breaks
        segments = self._calculate_segments(
            distance_miles, 
            base_driving_time, 
            num_fuel_stops,
            start_time
        )
        
        # Generate daily logs
        daily_logs = self._generate_daily_logs(segments, start_time)
        
        return {
            'total_distance': distance_miles,
            'total_driving_time': base_driving_time,
            'total_on_duty_time': total_on_duty_time,
            'estimated_duration_hours': self._calculate_total_duration(segments),
            'num_rest_breaks': len([s for s in segments if s['type'] == 'rest']),
            'num_fuel_stops': num_fuel_stops,
            'segments': segments,
            'daily_logs': daily_logs,
            'cycle_hours_used': self.current_cycle_used,
            'cycle_hours_available': self.available_cycle_hours
        }
    
    def _calculate_segments(self, total_distance: float, driving_time: float, 
                           num_fuel_stops: int, start_time: datetime) -> List[Dict]:
        """
        Break trip into segments with driving, rest, and fuel stops
        """
        segments = []
        current_time = start_time
        remaining_distance = total_distance
        remaining_driving_time = driving_time
        current_day_driving = 0
        current_day_on_duty = 0
        fuel_stops_remaining = num_fuel_stops
        
        # Add pickup activity
        segments.append({
            'type': 'on_duty',
            'activity': 'Pickup',
            'start_time': current_time.isoformat(),
            'duration': self.PICKUP_DROPOFF_DURATION,
            'distance': 0
        })
        current_time = self._safe_add_time(current_time, self.PICKUP_DROPOFF_DURATION)
        current_day_on_duty += self.PICKUP_DROPOFF_DURATION
        
        # Safety counter to prevent infinite loops
        max_iterations = 100  # Reduced from 1000 - a 1400 mile trip should not need 100 iterations
        iteration_count = 0
        
        while remaining_distance > 0.5 and iteration_count < max_iterations:  # Changed from > 0 to > 0.5
            iteration_count += 1
            # Calculate how much we can drive before hitting limits
            max_driving_today = min(
                self.MAX_DRIVING_HOURS - current_day_driving,
                remaining_driving_time
            )
            
            # Check on-duty limit
            max_on_duty_today = self.MAX_ON_DUTY_HOURS - current_day_on_duty
            if max_on_duty_today <= 0:
                # Need rest break
                segments.append({
                    'type': 'rest',
                    'activity': 'Off Duty - Rest Break',
                    'start_time': current_time.isoformat(),
                    'duration': self.MIN_REST_HOURS,
                    'distance': 0
                })
                current_time = self._safe_add_time(current_time, self.MIN_REST_HOURS)
                current_day_driving = 0
                current_day_on_duty = 0
                continue
            
            # Adjust for on-duty limit
            max_driving_today = min(max_driving_today, max_on_duty_today)
            
            if max_driving_today <= 0.1:  # Changed from <= 0 to <= 0.1 to avoid tiny segments
                # Need rest break
                segments.append({
                    'type': 'rest',
                    'activity': 'Off Duty - Rest Break',
                    'start_time': current_time.isoformat(),
                    'duration': self.MIN_REST_HOURS,
                    'distance': 0
                })
                current_time = self._safe_add_time(current_time, self.MIN_REST_HOURS)
                current_day_driving = 0
                current_day_on_duty = 0
                continue
            
            # Calculate segment distance
            segment_distance = min(
                max_driving_today * self.AVG_SPEED_MPH,
                remaining_distance
            )
            segment_time = segment_distance / self.AVG_SPEED_MPH
            
            # Skip if segment is too small (less than 0.1 hours = 6 minutes)
            if segment_time < 0.1:
                # Just finish the remaining distance
                if remaining_distance > 0:
                    remaining_distance = 0
                break
            
            # Check if we need a fuel stop in this segment
            if fuel_stops_remaining > 0 and segment_distance >= self.FUEL_INTERVAL_MILES * 0.8:
                # Split segment for fuel stop
                fuel_distance = self.FUEL_INTERVAL_MILES
                fuel_time = fuel_distance / self.AVG_SPEED_MPH
                
                # Driving to fuel stop
                segments.append({
                    'type': 'driving',
                    'activity': 'Driving',
                    'start_time': current_time.isoformat(),
                    'duration': fuel_time,
                    'distance': fuel_distance
                })
                current_time = self._safe_add_time(current_time, fuel_time)
                current_day_driving += fuel_time
                current_day_on_duty += fuel_time
                
                # Fuel stop
                segments.append({
                    'type': 'on_duty',
                    'activity': 'Fuel Stop',
                    'start_time': current_time.isoformat(),
                    'duration': self.FUEL_STOP_DURATION,
                    'distance': 0
                })
                current_time = self._safe_add_time(current_time, self.FUEL_STOP_DURATION)
                current_day_on_duty += self.FUEL_STOP_DURATION
                
                remaining_distance -= fuel_distance
                remaining_driving_time -= fuel_time
                fuel_stops_remaining -= 1
            else:
                # Regular driving segment
                segments.append({
                    'type': 'driving',
                    'activity': 'Driving',
                    'start_time': current_time.isoformat(),
                    'duration': segment_time,
                    'distance': segment_distance
                })
                current_time = self._safe_add_time(current_time, segment_time)
                current_day_driving += segment_time
                current_day_on_duty += segment_time
                
                remaining_distance -= segment_distance
                remaining_driving_time -= segment_time
        
        # Check if we hit iteration limit
        if iteration_count >= max_iterations:
            print(f"WARNING: Hit max iterations. Remaining distance: {remaining_distance:.1f} miles")
        
        # Add dropoff activity
        segments.append({
            'type': 'on_duty',
            'activity': 'Dropoff',
            'start_time': current_time.isoformat(),
            'duration': self.PICKUP_DROPOFF_DURATION,
            'distance': 0
        })
        
        return segments
    
    def _calculate_total_duration(self, segments: List[Dict]) -> float:
        """Calculate total trip duration including all segments"""
        return sum(s['duration'] for s in segments)
    
    def _generate_daily_logs(self, segments: List[Dict], start_time: datetime) -> List[Dict]:
        """
        Generate daily ELD logs from trip segments
        Each log represents a 24-hour period
        """
        daily_logs = []
        current_log = None
        current_date = start_time.date()
        max_days = 30  # Limit to 30 days max
        
        for segment in segments:
            try:
                # Parse ISO format, handle timezone if present
                segment_start_str = segment['start_time']
                if 'T' in segment_start_str:
                    segment_start = datetime.fromisoformat(segment_start_str.replace('Z', '+00:00'))
                else:
                    segment_start = datetime.fromisoformat(segment_start_str)
                segment_date = segment_start.date()
            except (ValueError, AttributeError) as e:
                # If parsing fails, use current date
                segment_date = current_date
                segment_start = datetime.combine(current_date, datetime.min.time())
            
            # Create new log if date changed or first segment
            if current_log is None or segment_date != current_date:
                if current_log:
                    daily_logs.append(current_log)
                
                # Stop if we've reached max days
                if len(daily_logs) >= max_days:
                    break
                
                current_date = segment_date
                # Validate date is in valid range
                try:
                    if current_date.year < MINYEAR or current_date.year > MAXYEAR:
                        current_date = start_time.date()
                    date_str = current_date.isoformat()
                except (ValueError, AttributeError, OverflowError):
                    current_date = start_time.date()
                    date_str = current_date.isoformat()
                
                current_log = {
                    'date': date_str,
                    'total_miles': 0,
                    'driving_hours': 0,
                    'on_duty_hours': 0,
                    'off_duty_hours': 0,
                    'sleeper_hours': 0,
                    'timeline': []
                }
            
            # Add segment to timeline
            timeline_entry = {
                'start_time': segment['start_time'],
                'duration': segment['duration'],
                'status': self._map_segment_to_status(segment['type']),
                'activity': segment['activity'],
                'distance': segment.get('distance', 0)
            }
            current_log['timeline'].append(timeline_entry)
            
            # Update totals
            current_log['total_miles'] += segment.get('distance', 0)
            
            if segment['type'] == 'driving':
                current_log['driving_hours'] += segment['duration']
                current_log['on_duty_hours'] += segment['duration']
            elif segment['type'] == 'on_duty':
                current_log['on_duty_hours'] += segment['duration']
            elif segment['type'] == 'rest':
                current_log['off_duty_hours'] += segment['duration']
        
        # Add final log
        if current_log:
            # Fill remaining hours as off duty
            total_hours = (current_log['driving_hours'] + 
                          current_log['on_duty_hours'] + 
                          current_log['off_duty_hours'])
            if total_hours < 24:
                current_log['off_duty_hours'] += (24 - total_hours)
            
            daily_logs.append(current_log)
        
        return daily_logs
    
    def _map_segment_to_status(self, segment_type: str) -> int:
        """
        Map segment type to ELD status code
        1: Off Duty, 2: Sleeper Berth, 3: Driving, 4: On Duty Not Driving
        """
        mapping = {
            'rest': 1,  # Off Duty
            'driving': 3,  # Driving
            'on_duty': 4  # On Duty Not Driving
        }
        return mapping.get(segment_type, 1)
