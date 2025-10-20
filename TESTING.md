# Testing Guide

## Manual Testing Checklist

### Backend API Testing

#### 1. Health Check
```bash
curl http://localhost:8000/api/health/
```
Expected: `{"status": "healthy", "timestamp": "..."}`

#### 2. Geocoding Test
```bash
curl -X POST http://localhost:8000/api/geocode/ \
  -H "Content-Type: application/json" \
  -d '{"address": "Los Angeles, CA"}'
```
Expected: Coordinates for Los Angeles

#### 3. Trip Calculation Test
```bash
curl -X POST http://localhost:8000/api/calculate-trip/ \
  -H "Content-Type: application/json" \
  -d '{
    "current_location": "Los Angeles, CA",
    "pickup_location": "Phoenix, AZ",
    "dropoff_location": "Dallas, TX",
    "current_cycle_used": 0
  }'
```
Expected: Complete trip data with route, segments, and log sheets

### Frontend Testing

#### Test Case 1: Short Trip (Same Day)
- **Current**: Los Angeles, CA
- **Pickup**: San Diego, CA
- **Dropoff**: Las Vegas, NV
- **Cycle**: 0
- **Expected**: 1 day trip, 1-2 rest breaks, 1 fuel stop

#### Test Case 2: Medium Trip (2-3 Days)
- **Current**: Los Angeles, CA
- **Pickup**: Phoenix, AZ
- **Dropoff**: Dallas, TX
- **Cycle**: 0
- **Expected**: 2-3 day trip, multiple rest breaks, 2-3 fuel stops

#### Test Case 3: Long Trip (4+ Days)
- **Current**: Seattle, WA
- **Pickup**: Portland, OR
- **Dropoff**: Miami, FL
- **Cycle**: 0
- **Expected**: 4+ day trip, many rest breaks, multiple fuel stops

#### Test Case 4: High Cycle Hours
- **Current**: Los Angeles, CA
- **Pickup**: Phoenix, AZ
- **Dropoff**: Dallas, TX
- **Cycle**: 60
- **Expected**: Trip calculated with limited available hours

### UI/UX Testing

#### Map Display
- [ ] Map loads correctly
- [ ] All three markers are visible (current, pickup, dropoff)
- [ ] Route polylines are drawn
- [ ] Map auto-zooms to fit all points
- [ ] Markers have correct colors
- [ ] Popups show correct information

#### Trip Form
- [ ] All input fields are present
- [ ] Validation works (required fields)
- [ ] Number input accepts decimals
- [ ] Loading state shows during calculation
- [ ] Error messages display correctly

#### Trip Summary
- [ ] All statistics display correctly
- [ ] Segments list is scrollable
- [ ] Hours are formatted properly
- [ ] Colors match segment types

#### ELD Logs
- [ ] Log sheets render correctly
- [ ] Navigation between days works
- [ ] Download button works
- [ ] Timeline shows all activities
- [ ] Statistics match the log sheet

#### Tabs
- [ ] All three tabs are accessible
- [ ] Tab switching works smoothly
- [ ] Content updates correctly

#### Responsive Design
- [ ] Desktop view (1920x1080)
- [ ] Tablet view (768x1024)
- [ ] Mobile view (375x667)
- [ ] All components are readable
- [ ] No horizontal scrolling

### Error Handling

#### Test Invalid Inputs
1. Empty location fields
   - Expected: Form validation error

2. Invalid address
   - Expected: "Could not geocode address" error

3. Cycle hours > 70
   - Expected: Form validation or backend error

4. Negative cycle hours
   - Expected: Form validation error

5. Backend offline
   - Expected: "Failed to calculate trip" error

### Performance Testing

#### Response Times
- [ ] Geocoding: < 2 seconds
- [ ] Route calculation: < 5 seconds
- [ ] Trip calculation: < 10 seconds
- [ ] Log generation: < 3 seconds

#### Load Testing
- [ ] Multiple concurrent requests
- [ ] Large distance trips (3000+ miles)
- [ ] Many segments (10+ days)

### Browser Compatibility

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### Accessibility Testing

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible
- [ ] Alt text for images

## Automated Testing

### Backend Unit Tests (Future)
```python
# backend/trip_planner/tests.py
from django.test import TestCase
from .eld_service import ELDService

class ELDServiceTests(TestCase):
    def test_calculate_trip_plan(self):
        service = ELDService(0)
        result = service.calculate_trip_plan(1000)
        self.assertGreater(result['total_driving_time'], 0)
        self.assertGreater(len(result['segments']), 0)
```

### Frontend Unit Tests (Future)
```javascript
// frontend/src/components/__tests__/TripForm.test.js
import { render, screen } from '@testing-library/react';
import TripForm from '../TripForm';

test('renders trip form', () => {
  render(<TripForm onSubmit={() => {}} loading={false} />);
  expect(screen.getByText(/Current Location/i)).toBeInTheDocument();
});
```

## Known Issues & Limitations

1. **Routing API**: Using free OSRM, may have rate limits
2. **Geocoding**: Nominatim has usage policy, may need delays between requests
3. **Log Generation**: Uses basic PIL, could be enhanced with better graphics
4. **Route Accuracy**: Simplified calculations, real routes may vary
5. **HOS Rules**: Implements basic rules, real scenarios may be more complex

## Bug Reporting

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots
- Browser/OS information
- Console errors
- Network tab information

## Performance Optimization Checklist

- [ ] Backend caching for geocoding results
- [ ] Frontend memoization for expensive calculations
- [ ] Lazy loading for map components
- [ ] Image optimization for log sheets
- [ ] API request debouncing
- [ ] Error boundary implementation
- [ ] Loading state optimization
