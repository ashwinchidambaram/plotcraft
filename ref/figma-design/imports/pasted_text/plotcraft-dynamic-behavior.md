ollow-up: Dynamic Behavior Rules & Layout Logic for PlotCraft Design System                                                                    
                                                                                                                                                  
  Now that the visual style is defined, I need you to design how the system behaves when content changes. These aren't static mockups — shapes    
  resize, text wraps, and layout adapts. Please create reference frames showing each of these behaviors.                                          
  
  1. Dynamic Shape Scaling                                                                                                                        
                                                                  
  Shapes auto-size to fit their text content. Design frames showing how each shape type grows:                                                    
  
  Rectangle:                                                                                                                                      
  - Show 3 versions side by side: short text ("OK"), medium text ("Build & Test"), and long text ("Deploy to Production Environment")
  - The rectangle should grow horizontally to fit, with consistent padding on all sides (define the padding value)                   
  - Show the minimum size (even with tiny text, the shape shouldn't be smaller than X)
  - When text is very long, it wraps to multiple lines and the rectangle grows vertically instead                                                 
  
  Square:                                                                                                                                         
  - Same 3 text lengths — the square always maintains equal width and height
  - It sizes to the larger dimension needed, so short wide text and tall narrow text both produce different sized squares                         
  
  Circle:                                                                                                                                         
  - Show how the circle's diameter grows to contain text          
  - The text sits inside the inscribed area — show the relationship between circle radius and text bounding box
                                                                                                               
  Diamond:
  - Show how the diamond scales — text lives in the inscribed rectangle of the diamond                                                            
  - The diamond needs to be roughly 1.5x the text area to contain it comfortably
  - Show short vs long text versions                                                                                                              
                                                                  
  Oval:
  - Show horizontal growth for wider text
  - The oval should maintain a pleasant aspect ratio (roughly 1.4:1 width-to-height minimum)
                                                                                            
  For all shapes: show a subtle dotted outline around each shape representing its bounding box — the invisible margin that prevents other shapes  
  from overlapping. The bounding box is slightly larger than the visible shape.                                                                   
                                                                                                                                                  
  2. Stroke Weight & Line Quality                                                                                                                 
                                                                  
  All shape outlines should use a consistent "normal pen" stroke weight — visible and confident, not thin/hairline and not chunky/bold. This is   
  the default stroke for every shape in the system.
                                                                                                                                                  
  Design a reference frame showing:                                                                                                               
  - The chosen stroke weight applied to every shape type (rect, square, circle, oval, diamond) side by side
  - A comparison strip: 0.5px (too thin), 1px (light pencil), the chosen weight (normal pen — likely 1.5-2px for sketch style), 3px (marker/bold) 
  - The "normal pen" weight should feel like a real pen on paper — confident single stroke, not timid, not shouting                              
  - This same weight is the default for all shape outlines, section borders, and connector lines                                                  
  - Bold and thin connector variants should be shown relative to this baseline                                                                    
                                                                                                                                                  
  3. Text Positioning & Justification                                                                                                             
                                                                                                                                                  
  Text inside shapes supports full 2D alignment control. The LLM chooses horizontal and vertical alignment independently.                         
                                                                  
  Horizontal alignment (3 options):                                                                                                               
  Show the same multi-line text ("Deploy to\nProduction\nEnvironment") inside a wide rectangle three times:
  - Left-aligned — each line starts at the left padding edge
  - Center-aligned — each line centered horizontally (default)                                                                                    
  - Right-aligned — each line ends at the right padding edge
                                                                                                                                                  
  Vertical alignment (3 options):                                 
  Show the same single line of text ("Status") inside a tall rectangle three times:
  - Top — text hugs the top padding edge                                                                                                          
  - Middle — text centered vertically (default)
  - Bottom — text sits at the bottom padding edge                                                                                                 
                                                                  
  Combined grid (3x3):                                                                                                                            
  Show a 3x3 matrix of rectangles (all same size, all with the same 2-line text), demonstrating every combination:
                                                                                                                                                  
  ┌────────┬─────────────┬───────────────┬──────────────┐                                                                                         
  │        │    Left     │    Center     │    Right     │                                                                                         
  ├────────┼─────────────┼───────────────┼──────────────┤                                                                                         
  │ Top    │ top-left    │ top-center    │ top-right    │         
  ├────────┼─────────────┼───────────────┼──────────────┤
  │ Middle │ middle-left │ middle-center │ middle-right │
  ├────────┼─────────────┼───────────────┼──────────────┤
  │ Bottom │ bottom-left │ bottom-center │ bottom-right │
  └────────┴─────────────┴───────────────┴──────────────┘                                                                                         
   
  This 3x3 grid is critical — it shows every possible text position within a shape. Label each cell clearly. Middle-Center is the default.        
                                                                  
  Text wrapping behavior:                                                                                                                         
  - Show a rectangle with a max text width of ~200px              
  - Short text: single line, shape is compact       
  - Medium text: wraps to 2 lines, shape grows taller
  - Long text: wraps to 3-4 lines, shape continues growing vertically
  - Show where the line breaks happen (word boundaries, never mid-word)                                                                           
                                                                       
  4. Role-Based Visual Hierarchy                                                                                                                  
                                                                                                                                                  
  Different text roles get different minimum sizes and padding, creating visual importance:
                                                                                                                                                  
  Show all 4 roles with the same short text ("Status") side by side:
  - Title — largest minimum size (280x80), most padding (1.8x), biggest font. This dominates the diagram.
  - Subtitle — medium-large minimum (220x60), moderate padding (1.4x). Secondary headings.                                                        
  - Body — no minimum size, standard padding (1.0x). Normal node text — sizes purely from content.
  - Caption — no minimum size, reduced padding (0.8x), smallest font. Annotations, labels.                                                        
                                                                  
  Show how a Title with just "Hi" is still a large, prominent shape, while a Body with "Hi" is compact. The role defines the visual weight, not   
  just the font size.
                                                                                                                                                  
  5. Grid Snapping & Spacing                                                                                                                      
   
  All shapes snap to an invisible grid. Show:                                                                                                     
                                                                  
  - A 4x3 grid with gridlines visible (dashed, very light)
  - Shapes placed at different grid positions — each shape's center aligns to its grid cell's center
  - A large shape (Title) that spans 2 grid columns — show how it occupies multiple cells
  - Two shapes in adjacent cells — show the guaranteed gap between their bounding boxes (they never overlap)                                      
  - Show the grid cell dimensions labeled (width, height, margin)
                                                                                                                                                  
  Auto-placement flow:                                                                                                                            
  - Show 6 shapes being auto-placed: they fill left-to-right, then wrap to the next row (like text in a paragraph)
  - Number them 1-6 to show the placement order                                                                                                   
                                                                  
  6. Connector Attachment Points (Anchors)
                                                                                                                                                  
  Every shape has 9 anchor points where connectors can attach. Show:
                                                                                                                                                  
  - A rectangle with all 9 anchor points marked as small dots:    
    - Top: left, center, right
    - Middle: left, center, right
    - Bottom: left, center, right
  - Label each anchor point                                                                                                                       
  - Show the same 9 points on a circle, oval, and diamond — the anchors map to the shape's actual edge, not the bounding box
                                                                                                                                                  
  7. Connector Routing Styles                                                                                                                     
   
  Connectors support two routing styles. Design reference frames for both:                                                                        
                                                                  
  Curved connectors (cubic bezier):                                                                                                               
  - Show a smooth S-curve connection between two shapes (right-center to left-center)
  - Show a vertical curve (bottom-center to top-center)                                                                                           
  - Show how the curve adjusts when shapes are at different angles — the curve always feels natural, never kinked
  - Show control point handles (lightly, for reference) so the bezier logic is clear                                                              
  - Curves should feel like a confident pen stroke, smooth and fluid                                                                              
                                                                                                                                                  
  Bent/orthogonal connectors (right-angle routing):                                                                                               
  - Show a connector that travels horizontally, turns 90 degrees, then travels vertically to reach its target                                     
  - Show L-shaped routes (one bend) and Z-shaped routes (two bends)                                                                               
  - Corners should have a small radius (not sharp 90-degree angles — matches the sketch aesthetic)                                                
  - Show how the bend point is calculated: typically midpoint between source and target on the primary axis                                       
                                                                                                                                                  
  Both styles side by side:                                                                                                                       
  - Show the same two shapes connected with a curved connector on the left and a bent connector on the right                                      
  - Label which style is which                                                                                                                    
                                                                  
  Multi-segment connectors:                                                                                                                       
  - Show a connector that needs to route around an obstacle — it adds intermediate waypoints
  - The path should feel intentional, not chaotic                                                                                                 
                                                                  
  8. Connector Label Positioning                                                                                                                  
                                                                  
  Show how labels sit relative to connectors:

  - A connector with a label — the label sits at the midpoint of the curve, offset perpendicular to the line direction (not on top of the line)   
  - Show the label has a small background (matching canvas color) so it doesn't collide with the line
  - Show 3 connectors at different angles — the label always stays readable (never upside down) and always offsets to the side                    
                                                                                                                                                  
  9. Boundary & Overlap Rules (Critical)                                                                                                          
                                                                                                                                                  
  This is the most important layout rule in the entire system. Design a reference frame that makes these rules crystal clear:                     
                                                                  
  Rule 1: No shape may overlap any other shape.                                                                                                   
  - Show two shapes close together with their bounding boxes visible (dotted outlines)
  - The bounding boxes have clear space between them — they never touch or overlap                                                                
  - Show an "incorrect" version (red X) with overlapping bounding boxes, and a "correct" version (green check) with proper spacing
                                                                                                                                                  
  Rule 2: No shape may overlap any text.                                                                                                          
  - Show a shape near free-floating text — the text has its own (smaller) bounding box                                                            
  - The shape's bounding box and the text's bounding box do not overlap                                                                           
                                                                       
  Rule 3: Connector lines may cross bounding box margins.                                                                                         
  - Show a connector line passing through the bounding box margin area (the space between the visible shape and the bounding box edge) — this is  
  allowed                                                                                                                                         
  - But show that the connector line never crosses through the visible shape itself or its text                                                   
  - Show a "correct" routing: connector enters bounding box margin, curves around the shape edge, exits the other side                            
  - Show an "incorrect" version: connector cutting straight through a shape (red X)                                                               
                                                                                                                                                  
  Rule 4: Connector lines may cross each other.                                                                                                   
  - Show two connectors crossing — this is fine and sometimes unavoidable                                                                         
  - At the crossing point, one line continues over the other (no special treatment needed in sketch style)                                        
                                                                  
  Summary diagram:                                                                                                                                
  Create one frame showing all 4 rules in action together:        
  - 4-5 shapes placed on the grid with visible bounding boxes                                                                                     
  - Multiple connectors routing between them                                                                                                      
  - Connectors routed AROUND shapes (never through)                                                                                               
  - Two connectors crossing each other (acceptable)                                                                                               
  - Clear gaps between all bounding boxes (no shape overlaps)     
  - Free-floating text labels with their own bounding boxes, not overlapped by any shape                                                          
                                                                                                                                                  
  Label this frame "Boundary Rules — The Golden Rules of PlotCraft Layout" or similar.                                                            
                                                                                                                                                  
  10. Section Container Behavior                                                                                                                  
                                                                                                                                                  
  Sections dynamically size around their contained shapes:        

  - Show a section with 2 shapes — the section background extends with padding around both shapes                                                 
  - Add a third shape to the section — show how the section grows to encompass it
  - The section label stays pinned to the top-left inside corner                                                                                  
  - Show that section backgrounds render behind shapes and connectors (z-order: sections → connectors → shapes)

  11. Implementation Component Library                                                                                                            
  
  Design a component/symbol library frame that serves as a copy-paste reference for building diagrams. Organize it like a toolbox:                
                                                                  
  Shape components (one of each, in Neutral):                                                                                                     
  - Rectangle, Square, Circle, Oval, Diamond, Free-floating text  
  - Each labeled with its type name below                                                                                                         
                                                                  
  Shape components (Rectangle in all 9 color themes):                                                                                             
  - 9 rectangles in a row, each with its theme name inside        
                                                                                                                                                  
  Connector components:                                           
  - Solid / Dashed / Dotted — horizontal, with labels                                                                                             
  - Thin / Normal / Bold — horizontal, with labels                
  - Forward arrow / Backward arrow / Bidirectional / No arrow — horizontal, with labels                                                           
                                                                                                                                                  
  Anchor point reference:
  - One rectangle with all 9 anchors labeled                                                                                                      
                                                                  
  Text role samples:                                                                                                                              
  - Title / Subtitle / Body / Caption — stacked vertically with labels                                                                            
  
  Text justification reference:                                                                                                                   
  - The 3x3 alignment grid from Section 3                         
                                                                                                                                                  
  Section container samples:
  - 3 section backgrounds in different color schemes                                                                                              
                                                                                                                                                  
  Boundary rule cheat sheet:
  - Compact version of Section 9's rules as a quick visual reference                                                                              
                                                                                                                                                  
  This component library frame should be a one-stop reference — when building any new diagram, you grab components from here and know exactly how 
  they'll behave.                                                                                                                                 
                                                                  
  12. Edge Cases to Show                                                                                                                          
                                                                  
  Design how these tricky situations should look:

  - Empty text — a shape with "" empty string (should still have minimum size, just no visible text)                                              
  - Very long single word — "Supercalifragilisticexpialidocious" in a rectangle (does it stretch wide or force-break?)
  - Many lines — 5+ lines of wrapped text in a rectangle (how tall does it get?)                                                                  
  - Overlapping section boundaries — two sections whose shapes are close together (sections should not overlap)                                   
  - Dense connections — one shape with 4+ connectors attached to different anchors (should still be readable)