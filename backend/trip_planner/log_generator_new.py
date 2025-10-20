"""
ELD Log Sheet Generator - Matches Official FMCSA Format
Generates visual ELD log sheets matching the standard paper log format
"""
from datetime import datetime, timedelta
from typing import List, Dict
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import os


class ELDLogGenerator:
    """Generates visual ELD log sheets matching official FMCSA format"""
    
    # Log sheet dimensions (standard paper log size)
    WIDTH = 1400
    HEIGHT = 1000
    
    # Grid dimensions for 24-hour timeline
    GRID_START_X = 60
    GRID_START_Y = 350
    GRID_WIDTH = 1280  # ~53 pixels per hour (24 hours)
    GRID_HEIGHT = 200  # 50 pixels per status line (4 lines)
    
    # Status lines (from top to bottom) - matching official log
    STATUS_LINES = {
        1: {'name': '1. Off Duty', 'y_offset': 0},
        2: {'name': '2. Sleeper', 'y_offset': 50},
        3: {'name': '3. Driving', 'y_offset': 100},
        4: {'name': '4. On Duty', 'y_offset': 150}
    }
    
    def __init__(self):
        """Initialize log generator"""
        pass
    
    def generate_log_sheet(self, log_data: Dict, driver_name: str = "Driver") -> str:
        """
        Generate a single ELD log sheet matching official format
        
        Args:
            log_data: Daily log data with timeline
            driver_name: Driver's name
            
        Returns:
            Base64 encoded PNG image
        """
        # Create blank image
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        # Try to use fonts
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 20)
            header_font = ImageFont.truetype("arial.ttf", 14)
            label_font = ImageFont.truetype("arial.ttf", 11)
            small_font = ImageFont.truetype("arial.ttf", 9)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw all sections
        self._draw_header(draw, log_data, driver_name, title_font, header_font, label_font, small_font)
        self._draw_info_boxes(draw, log_data, label_font, small_font)
        self._draw_grid(draw, label_font, small_font)
        self._draw_timeline(draw, log_data['timeline'])
        self._draw_remarks(draw, label_font)
        self._draw_shipping_docs(draw, label_font, small_font)
        self._draw_certification(draw, log_data, label_font, small_font)
        
        # Convert to base64
        buffer = io.BytesIO()
        img = img.resize((1200, 850), Image.Resampling.LANCZOS)  # Scale down slightly
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return img_base64
    
    def _draw_header(self, draw, log_data: Dict, driver_name: str, 
                     title_font, header_font, label_font, small_font):
        """Draw log sheet header - top section"""
        # Title
        draw.text((20, 10), "Drivers Daily Log", fill='black', font=title_font)
        
        # Date boxes
        try:
            log_date = datetime.fromisoformat(log_data['date'])
            month = log_date.strftime('%m')
            day = log_date.strftime('%d')
            year = log_date.strftime('%Y')
        except:
            month = datetime.now().strftime('%m')
            day = datetime.now().strftime('%d')
            year = datetime.now().strftime('%Y')
        
        # Date fields
        x_start = 200
        draw.text((x_start, 15), "(month)", fill='black', font=small_font)
        draw.text((x_start + 60, 15), "(day)", fill='black', font=small_font)
        draw.text((x_start + 110, 15), "(year)", fill='black', font=small_font)
        
        # Date boxes
        draw.rectangle([(x_start, 30), (x_start + 50, 55)], outline='black', width=1)
        draw.text((x_start + 15, 35), month, fill='black', font=header_font)
        
        draw.text((x_start + 55, 40), "/", fill='black', font=header_font)
        
        draw.rectangle([(x_start + 60, 30), (x_start + 110, 55)], outline='black', width=1)
        draw.text((x_start + 75, 35), day, fill='black', font=header_font)
        
        draw.text((x_start + 115, 40), "/", fill='black', font=header_font)
        
        draw.rectangle([(x_start + 125, 30), (x_start + 200, 55)], outline='black', width=1)
        draw.text((x_start + 145, 35), year, fill='black', font=header_font)
        
        # Right side - Original/Duplicate
        draw.text((900, 10), "Original - File at home terminal", fill='black', font=small_font)
        draw.text((900, 25), "Duplicate - Driver retains for 7 days", fill='black', font=small_font)
        
        # 24 hours line
        draw.text((20, 60), "24 hours", fill='black', font=label_font)
        
        # From box
        draw.text((20, 85), "From:", fill='black', font=label_font)
        draw.rectangle([(70, 80), (250, 110)], outline='black', width=1)
    
    def _draw_info_boxes(self, draw, log_data: Dict, label_font, small_font):
        """Draw information boxes below header"""
        y_start = 120
        
        # Row 1 - Miles boxes
        # Total Miles Driving Today
        draw.rectangle([(20, y_start), (180, y_start + 50)], outline='black', width=2)
        draw.text((25, y_start + 5), "Total Miles Driving Today", fill='black', font=small_font)
        draw.text((60, y_start + 25), f"{log_data['total_miles']:.0f}", fill='black', font=label_font)
        
        # Total Mileage Today
        draw.rectangle([(185, y_start), (345, y_start + 50)], outline='black', width=2)
        draw.text((190, y_start + 5), "Total Mileage Today", fill='black', font=small_font)
        draw.text((230, y_start + 25), f"{log_data['total_miles']:.0f}", fill='black', font=label_font)
        
        # Name of Carrier or Carriers
        draw.text((700, y_start + 5), "Name of Carrier or Carriers", fill='black', font=small_font)
        draw.line([(700, y_start + 25), (1100, y_start + 25)], fill='black', width=1)
        
        # Row 2 - License info
        y_start2 = y_start + 55
        draw.rectangle([(20, y_start2), (345, y_start2 + 50)], outline='black', width=2)
        draw.text((25, y_start2 + 5), "Truck/Tractor and Trailer Numbers or", fill='black', font=small_font)
        draw.text((25, y_start2 + 20), "License Plate(s)/State (show each unit)", fill='black', font=small_font)
        
        # Main Office Address
        draw.text((700, y_start2 + 5), "Main Office Address", fill='black', font=small_font)
        draw.line([(700, y_start2 + 25), (1100, y_start2 + 25)], fill='black', width=1)
        
        # Home Terminal Address
        draw.text((700, y_start2 + 35), "Home Terminal Address", fill='black', font=small_font)
        draw.line([(700, y_start2 + 55), (1100, y_start2 + 55)], fill='black', width=1)
    
    def _draw_grid(self, draw, label_font, small_font):
        """Draw the 24-hour grid with status lines"""
        # Draw status line labels on left
        for status_num, status_info in self.STATUS_LINES.items():
            y = self.GRID_START_Y + status_info['y_offset']
            draw.text((10, y + 15), status_info['name'], fill='black', font=small_font)
        
        # Draw main grid border
        draw.rectangle([
            (self.GRID_START_X, self.GRID_START_Y),
            (self.GRID_START_X + self.GRID_WIDTH, self.GRID_START_Y + self.GRID_HEIGHT)
        ], outline='black', width=2)
        
        # Draw horizontal lines between status rows
        for i in range(1, 4):
            y = self.GRID_START_Y + (i * 50)
            draw.line([
                (self.GRID_START_X, y),
                (self.GRID_START_X + self.GRID_WIDTH, y)
            ], fill='black', width=1)
        
        # Draw vertical lines for each hour
        hour_width = self.GRID_WIDTH / 24
        for hour in range(25):  # 0 to 24
            x = self.GRID_START_X + (hour * hour_width)
            # Thicker line every 2 hours
            line_width = 2 if hour % 2 == 0 else 1
            draw.line([
                (x, self.GRID_START_Y),
                (x, self.GRID_START_Y + self.GRID_HEIGHT)
            ], fill='black', width=line_width)
        
        # Draw hour labels at top
        y_label = self.GRID_START_Y - 20
        draw.text((self.GRID_START_X - 30, y_label), "Mid-", fill='black', font=small_font)
        draw.text((self.GRID_START_X - 30, y_label + 10), "night", fill='black', font=small_font)
        
        for hour in range(1, 12):
            x = self.GRID_START_X + (hour * hour_width) - 5
            draw.text((x, y_label), str(hour), fill='black', font=small_font)
        
        x_noon = self.GRID_START_X + (12 * hour_width) - 10
        draw.text((x_noon, y_label), "Noon", fill='black', font=small_font)
        
        for hour in range(1, 12):
            x = self.GRID_START_X + ((12 + hour) * hour_width) - 5
            draw.text((x, y_label), str(hour), fill='black', font=small_font)
        
        x_midnight = self.GRID_START_X + (24 * hour_width) - 30
        draw.text((x_midnight, y_label), "Mid-", fill='black', font=small_font)
        draw.text((x_midnight, y_label + 10), "night", fill='black', font=small_font)
        
        # Draw "Total Hours" label on right
        draw.text((self.GRID_START_X + self.GRID_WIDTH + 10, self.GRID_START_Y + 80), 
                 "Total", fill='black', font=small_font)
        draw.text((self.GRID_START_X + self.GRID_WIDTH + 10, self.GRID_START_Y + 92), 
                 "Hours", fill='black', font=small_font)
    
    def _draw_timeline(self, draw, timeline: List[Dict]):
        """Draw the activity timeline on the grid"""
        hour_width = self.GRID_WIDTH / 24
        
        for entry in timeline:
            try:
                start_time = datetime.fromisoformat(entry['start_time'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                start_time = datetime.now()
            
            duration = entry['duration']
            status = entry['status']
            
            # Calculate start hour (decimal)
            start_hour = start_time.hour + start_time.minute / 60.0
            
            # Calculate pixel positions
            start_x = self.GRID_START_X + int(start_hour * hour_width)
            width = int(duration * hour_width)
            
            # Get status line position
            status_info = self.STATUS_LINES.get(status, self.STATUS_LINES[1])
            y = self.GRID_START_Y + status_info['y_offset']
            
            # Draw filled rectangle for this activity
            draw.rectangle([
                (start_x, y + 2),
                (start_x + width, y + 48)
            ], fill='#4A90E2', outline='#2E5C8A', width=1)
    
    def _draw_remarks(self, draw, label_font):
        """Draw remarks section"""
        y_start = self.GRID_START_Y + self.GRID_HEIGHT + 20
        
        draw.text((20, y_start), "Remarks", fill='black', font=label_font)
        draw.rectangle([
            (20, y_start + 20),
            (700, y_start + 100)
        ], outline='black', width=1)
    
    def _draw_shipping_docs(self, draw, label_font, small_font):
        """Draw shipping documents section"""
        y_start = self.GRID_START_Y + self.GRID_HEIGHT + 130
        
        draw.text((20, y_start), "Shipping", fill='black', font=label_font)
        draw.text((20, y_start + 15), "Documents:", fill='black', font=label_font)
        
        draw.rectangle([
            (20, y_start + 35),
            (200, y_start + 65)
        ], outline='black', width=1)
        draw.text((25, y_start + 42), "Bill of Manifest No.", fill='black', font=small_font)
        
        draw.rectangle([
            (20, y_start + 70),
            (200, y_start + 100)
        ], outline='black', width=1)
        draw.text((25, y_start + 77), "Shipper & Commodity", fill='black', font=small_font)
        
        draw.text((25, y_start + 110), "Enter name of place you reported and where relieved from work and where each change of duty occurred.", 
                 fill='black', font=small_font)
    
    def _draw_certification(self, draw, log_data: Dict, label_font, small_font):
        """Draw certification section at bottom"""
        y_start = self.GRID_START_Y + self.GRID_HEIGHT + 270
        
        # Recap section
        draw.text((20, y_start), "Recap:", fill='black', font=label_font)
        draw.text((20, y_start + 15), "Off duty last 8", fill='black', font=small_font)
        draw.text((20, y_start + 27), "days", fill='black', font=small_font)
        
        # Hours table
        x_table = 120
        col_width = 80
        
        # Header
        draw.text((x_table, y_start), "70 Hour /", fill='black', font=small_font)
        draw.text((x_table, y_start + 12), "8 Day", fill='black', font=small_font)
        
        # Columns
        for i, label in enumerate(['A. Total', 'B. Total', 'C. Total']):
            x = x_table + (i + 1) * col_width
            draw.text((x, y_start + 5), label, fill='black', font=small_font)
        
        # Row labels
        rows = [
            ('On duty', 'hours on', 'hours on'),
            ('hours', 'duty', 'duty'),
            ('today', 'yesterday', 'tomorrow'),
            ('', '(minus A)', '(minus A)')
        ]
        
        for row_idx, row_labels in enumerate(rows):
            y_row = y_start + 30 + (row_idx * 12)
            for col_idx, text in enumerate(row_labels):
                x = x_table + col_idx * col_width
                draw.text((x, y_row), text, fill='black', font=small_font)
        
        # Totals
        draw.text((x_table + 20, y_start + 90), "Total", fill='black', font=small_font)
        draw.text((x_table + 20, y_start + 102), "time", fill='black', font=small_font)
        draw.text((x_table + 20, y_start + 114), "3 & 4", fill='black', font=small_font)
        
        # Right side - 60 hour section
        x_right = x_table + 350
        draw.text((x_right, y_start), "*If you took", fill='black', font=small_font)
        draw.text((x_right, y_start + 12), "consecutive", fill='black', font=small_font)
        draw.text((x_right, y_start + 24), "hours off", fill='black', font=small_font)
        
        # Signature line
        y_sig = y_start + 100
        draw.text((700, y_sig), "Driver's Signature/Certification", fill='black', font=small_font)
        draw.line([(700, y_sig + 20), (1100, y_sig + 20)], fill='black', width=1)
        
        draw.text((700, y_sig + 25), "I certify that my record of duty status for this date is true and correct.", 
                 fill='black', font=small_font)
    
    def generate_all_logs(self, daily_logs: List[Dict], driver_name: str = "Driver") -> List[str]:
        """
        Generate log sheets for all days
        
        Args:
            daily_logs: List of daily log data
            driver_name: Driver's name
            
        Returns:
            List of base64 encoded PNG images
        """
        return [self.generate_log_sheet(log, driver_name) for log in daily_logs]
    
    def _map_segment_to_status(self, segment_type: str) -> int:
        """Map segment type to status line number"""
        mapping = {
            'rest': 1,  # Off Duty
            'sleeper': 2,  # Sleeper
            'driving': 3,  # Driving
            'on_duty': 4  # On Duty
        }
        return mapping.get(segment_type, 1)
