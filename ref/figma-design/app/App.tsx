import { useState } from 'react';

// Helper function to add wobble to a path
const wobble = (x: number, y: number, intensity = 2) => {
  return {
    x: x + (Math.random() - 0.5) * intensity,
    y: y + (Math.random() - 0.5) * intensity
  };
};

// Generate wobbly rounded rectangle path
const generateWobblyRect = (width: number, height: number, radius: number) => {
  const points = [
    wobble(radius, 0, 1.5),
    wobble(width - radius, 0, 1.5),
    wobble(width, radius, 1.5),
    wobble(width, height - radius, 1.5),
    wobble(width - radius, height, 1.5),
    wobble(radius, height, 1.5),
    wobble(0, height - radius, 1.5),
    wobble(0, radius, 1.5)
  ];

  return `
    M ${points[0].x} ${points[0].y}
    L ${points[1].x} ${points[1].y}
    Q ${wobble(width, 0, 1).x} ${wobble(width, 0, 1).y} ${points[2].x} ${points[2].y}
    L ${points[3].x} ${points[3].y}
    Q ${wobble(width, height, 1).x} ${wobble(width, height, 1).y} ${points[4].x} ${points[4].y}
    L ${points[5].x} ${points[5].y}
    Q ${wobble(0, height, 1).x} ${wobble(0, height, 1).y} ${points[6].x} ${points[6].y}
    L ${points[7].x} ${points[7].y}
    Q ${wobble(0, 0, 1).x} ${wobble(0, 0, 1).y} ${points[0].x} ${points[0].y}
    Z
  `;
};

// Generate wobbly circle path
const generateWobblyCircle = (cx: number, cy: number, r: number) => {
  const points = 16;
  let path = '';
  for (let i = 0; i <= points; i++) {
    const angle = (i / points) * Math.PI * 2;
    const wobbleAmount = (Math.random() - 0.5) * 3;
    const radius = r + wobbleAmount;
    const x = cx + Math.cos(angle) * radius;
    const y = cy + Math.sin(angle) * radius;
    path += (i === 0 ? 'M' : 'L') + ` ${x} ${y} `;
  }
  path += 'Z';
  return path;
};

// Generate wobbly diamond path
const generateWobblyDiamond = (size: number) => {
  const center = size / 2;
  const top = wobble(center, 5, 2);
  const right = wobble(size - 5, center, 2);
  const bottom = wobble(center, size - 5, 2);
  const left = wobble(5, center, 2);

  return `M ${top.x} ${top.y} L ${right.x} ${right.y} L ${bottom.x} ${bottom.y} L ${left.x} ${left.y} Z`;
};

// Generate wobbly line
const generateWobblyLine = (x1: number, y1: number, x2: number, y2: number) => {
  const segments = 8;
  let path = `M ${x1} ${y1}`;

  for (let i = 1; i <= segments; i++) {
    const t = i / segments;
    const x = x1 + (x2 - x1) * t;
    const y = y1 + (y2 - y1) * t;
    const wobbled = wobble(x, y, 1.5);
    path += ` L ${wobbled.x} ${wobbled.y}`;
  }

  return path;
};

type ColorTheme = {
  name: string;
  fill: string;
  stroke: string;
};

const colorThemes: ColorTheme[] = [
  { name: 'Neutral', fill: 'var(--pc-neutral-fill)', stroke: 'var(--pc-neutral-stroke)' },
  { name: 'Start', fill: 'var(--pc-start-fill)', stroke: 'var(--pc-start-stroke)' },
  { name: 'End', fill: 'var(--pc-end-fill)', stroke: 'var(--pc-end-stroke)' },
  { name: 'Decision', fill: 'var(--pc-decision-fill)', stroke: 'var(--pc-decision-stroke)' },
  { name: 'Error', fill: 'var(--pc-error-fill)', stroke: 'var(--pc-error-stroke)' },
  { name: 'Highlight', fill: 'var(--pc-highlight-fill)', stroke: 'var(--pc-highlight-stroke)' },
  { name: 'Info', fill: 'var(--pc-info-fill)', stroke: 'var(--pc-info-stroke)' },
  { name: 'Success', fill: 'var(--pc-success-fill)', stroke: 'var(--pc-success-stroke)' },
  { name: 'Warning', fill: 'var(--pc-warning-fill)', stroke: 'var(--pc-warning-stroke)' },
];

// Shape component with wobbly rendering
const ShapeBox = ({
  theme,
  shape = 'rectangle',
  label,
  size = 'md'
}: {
  theme: ColorTheme;
  shape?: 'rectangle' | 'square' | 'circle' | 'oval' | 'diamond' | 'text';
  label: string;
  size?: 'sm' | 'md' | 'lg';
}) => {
  const [path] = useState(() => {
    if (shape === 'rectangle') return generateWobblyRect(180, 90, 12);
    if (shape === 'square') return generateWobblyRect(100, 100, 10);
    if (shape === 'circle') return generateWobblyCircle(50, 50, 45);
    if (shape === 'oval') return generateWobblyCircle(90, 45, 40);
    if (shape === 'diamond') return generateWobblyDiamond(100);
    return '';
  });

  const dimensions =
    shape === 'rectangle' ? { width: 180, height: 90 } :
    shape === 'square' ? { width: 100, height: 100 } :
    shape === 'circle' ? { width: 100, height: 100 } :
    shape === 'oval' ? { width: 180, height: 90 } :
    shape === 'diamond' ? { width: 100, height: 100 } :
    { width: 180, height: 90 };

  if (shape === 'text') {
    return (
      <div className="inline-block">
        <div
          style={{
            fontFamily: 'var(--pc-font-body)',
            fontSize: size === 'lg' ? '28px' : size === 'md' ? '18px' : '14px',
            color: theme.stroke,
          }}
        >
          {label}
        </div>
      </div>
    );
  }

  return (
    <div className="inline-block relative" style={{ margin: '10px' }}>
      <svg
        width={dimensions.width}
        height={dimensions.height}
        style={{ filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))' }}
      >
        <path
          d={path}
          fill={theme.fill}
          stroke={theme.stroke}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <text
          x={dimensions.width / 2}
          y={dimensions.height / 2}
          textAnchor="middle"
          dominantBaseline="middle"
          style={{
            fontFamily: 'var(--pc-font-body)',
            fontSize: size === 'lg' ? '22px' : size === 'md' ? '16px' : '12px',
            fill: theme.stroke,
            userSelect: 'none'
          }}
        >
          {label}
        </text>
      </svg>
    </div>
  );
};

// Section container component
const SectionBox = ({
  title,
  color,
  children
}: {
  title: string;
  color: 'neutral' | 'highlight' | 'info';
  children: React.ReactNode;
}) => {
  const [path] = useState(() => generateWobblyRect(400, 280, 16));

  const fills = {
    neutral: 'rgba(241, 238, 232, 0.3)',
    highlight: 'rgba(204, 221, 255, 0.2)',
    info: 'rgba(178, 236, 227, 0.2)'
  };

  const strokes = {
    neutral: 'rgba(90, 90, 82, 0.3)',
    highlight: 'rgba(107, 143, 204, 0.4)',
    info: 'rgba(77, 170, 154, 0.4)'
  };

  return (
    <div className="relative inline-block" style={{ margin: '20px' }}>
      <svg width="400" height="280" className="absolute inset-0">
        <path
          d={path}
          fill={fills[color]}
          stroke={strokes[color]}
          strokeWidth="2"
          strokeDasharray="5,5"
          strokeLinecap="round"
        />
      </svg>
      <div className="relative p-6">
        <div
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '20px',
            color: strokes[color].replace(/[0-9.]+\)/, '1)'),
            marginBottom: '16px'
          }}
        >
          {title}
        </div>
        {children}
      </div>
    </div>
  );
};

// Connector/Arrow component
const Connector = ({
  x1,
  y1,
  x2,
  y2,
  style = 'solid',
  weight = 'normal',
  arrow = 'forward',
  label
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  style?: 'solid' | 'dashed' | 'dotted';
  weight?: 'thin' | 'normal' | 'bold';
  arrow?: 'forward' | 'backward' | 'both' | 'none';
  label?: string;
}) => {
  const [path] = useState(() => generateWobblyLine(x1, y1, x2, y2));

  const strokeWidth = weight === 'thin' ? 1 : weight === 'bold' ? 3 : 2;
  const strokeDasharray =
    style === 'dashed' ? '8,6' :
    style === 'dotted' ? '2,4' :
    'none';

  const angle = Math.atan2(y2 - y1, x2 - x1);

  const ArrowHead = ({ x, y, rotation }: { x: number; y: number; rotation: number }) => {
    const size = 8;
    const p1 = wobble(x, y, 0.5);
    const p2 = wobble(
      x - size * Math.cos(rotation - Math.PI / 6),
      y - size * Math.sin(rotation - Math.PI / 6),
      0.5
    );
    const p3 = wobble(
      x - size * Math.cos(rotation + Math.PI / 6),
      y - size * Math.sin(rotation + Math.PI / 6),
      0.5
    );

    return (
      <path
        d={`M ${p1.x} ${p1.y} L ${p2.x} ${p2.y} L ${p3.x} ${p3.y} Z`}
        fill="var(--pc-neutral-stroke)"
        stroke="none"
      />
    );
  };

  const midX = (x1 + x2) / 2;
  const midY = (y1 + y2) / 2;

  return (
    <g>
      <path
        d={path}
        fill="none"
        stroke="var(--pc-neutral-stroke)"
        strokeWidth={strokeWidth}
        strokeDasharray={strokeDasharray}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {(arrow === 'forward' || arrow === 'both') && (
        <ArrowHead x={x2} y={y2} rotation={angle} />
      )}
      {(arrow === 'backward' || arrow === 'both') && (
        <ArrowHead x={x1} y={y1} rotation={angle + Math.PI} />
      )}
      {label && (
        <text
          x={midX}
          y={midY - 10}
          textAnchor="middle"
          style={{
            fontFamily: 'var(--pc-font-caption)',
            fontSize: '14px',
            fill: 'var(--pc-neutral-stroke)',
          }}
        >
          {label}
        </text>
      )}
    </g>
  );
};

// Behavior Sections Component
const BehaviorSections = () => {
  return (
    <>
      {/* 1. Dynamic Shape Scaling */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          1. Dynamic Shape Scaling
        </h2>
        <p
          style={{
            fontFamily: 'var(--pc-font-body)',
            fontSize: '16px',
            color: '#5a5a52',
            marginBottom: '24px'
          }}
        >
          Shapes auto-size to fit content with consistent padding (16px). Minimum size prevents tiny shapes.
        </p>

        {/* Rectangle Scaling */}
        <div className="mb-8">
          <h3
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '20px',
              color: '#5a5a52',
              marginBottom: '16px'
            }}
          >
            Rectangle — Horizontal Growth & Text Wrapping
          </h3>
          <div className="flex gap-8 items-center flex-wrap">
            <div className="text-center">
              <div className="relative inline-block" style={{ margin: '10px' }}>
                <svg width="80" height="70">
                  <path
                    d={generateWobblyRect(80, 60, 10)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                    strokeDasharray="3,3"
                    opacity="0.3"
                  />
                  <path
                    d={generateWobblyRect(70, 50, 10)}
                    transform="translate(5, 5)"
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text
                    x="40"
                    y="35"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-neutral-stroke)' }}
                  >
                    OK
                  </text>
                </svg>
              </div>
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                Short text<br/>Min size: 60x40px
              </div>
            </div>

            <div className="text-center">
              <div className="relative inline-block" style={{ margin: '10px' }}>
                <svg width="180" height="70">
                  <path
                    d={generateWobblyRect(180, 60, 10)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                    strokeDasharray="3,3"
                    opacity="0.3"
                  />
                  <path
                    d={generateWobblyRect(170, 50, 10)}
                    transform="translate(5, 5)"
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text
                    x="90"
                    y="35"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-neutral-stroke)' }}
                  >
                    Build & Test
                  </text>
                </svg>
              </div>
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                Medium text<br/>Grows horizontally
              </div>
            </div>

            <div className="text-center">
              <div className="relative inline-block" style={{ margin: '10px' }}>
                <svg width="240" height="110">
                  <path
                    d={generateWobblyRect(240, 100, 10)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                    strokeDasharray="3,3"
                    opacity="0.3"
                  />
                  <path
                    d={generateWobblyRect(230, 90, 10)}
                    transform="translate(5, 5)"
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text
                    x="120"
                    y="40"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-neutral-stroke)' }}
                  >
                    Deploy to Production
                  </text>
                  <text
                    x="120"
                    y="60"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-neutral-stroke)' }}
                  >
                    Environment
                  </text>
                </svg>
              </div>
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                Long text wraps<br/>Grows vertically
              </div>
            </div>
          </div>
        </div>

        {/* Other Shape Scaling */}
        <div className="mb-8">
          <h3
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '20px',
              color: '#5a5a52',
              marginBottom: '16px'
            }}
          >
            Other Shapes — Scaling Behavior
          </h3>
          <div className="flex gap-8 flex-wrap">
            <div className="text-center">
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', marginBottom: '8px', fontWeight: 600 }}>
                Square (maintains 1:1)
              </div>
              <div className="flex gap-4">
                <svg width="70" height="70">
                  <path
                    d={generateWobblyRect(60, 60, 10)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text x="30" y="30" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                    Hi
                  </text>
                </svg>
                <svg width="100" height="100">
                  <path
                    d={generateWobblyRect(90, 90, 10)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text x="45" y="45" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                    Medium
                  </text>
                </svg>
              </div>
            </div>

            <div className="text-center">
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', marginBottom: '8px', fontWeight: 600 }}>
                Circle (diameter grows)
              </div>
              <div className="flex gap-4">
                <svg width="70" height="70">
                  <path
                    d={generateWobblyCircle(35, 35, 30)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text x="35" y="35" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                    Go
                  </text>
                </svg>
                <svg width="110" height="110">
                  <path
                    d={generateWobblyCircle(55, 55, 50)}
                    fill="var(--pc-neutral-fill)"
                    stroke="var(--pc-neutral-stroke)"
                    strokeWidth="2"
                  />
                  <text x="55" y="55" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                    Process
                  </text>
                </svg>
              </div>
            </div>

            <div className="text-center">
              <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', marginBottom: '8px', fontWeight: 600 }}>
                Diamond (1.5x text area)
              </div>
              <div className="flex gap-4">
                <svg width="70" height="70">
                  <path
                    d={generateWobblyDiamond(60)}
                    fill="var(--pc-decision-fill)"
                    stroke="var(--pc-decision-stroke)"
                    strokeWidth="2"
                  />
                  <text x="30" y="30" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '12px', fill: 'var(--pc-decision-stroke)' }}>
                    Yes?
                  </text>
                </svg>
                <svg width="110" height="110">
                  <path
                    d={generateWobblyDiamond(100)}
                    fill="var(--pc-decision-fill)"
                    stroke="var(--pc-decision-stroke)"
                    strokeWidth="2"
                  />
                  <text x="50" y="50" textAnchor="middle" dominantBaseline="middle"
                    style={{ fontFamily: 'var(--pc-font-body)', fontSize: '12px', fill: 'var(--pc-decision-stroke)' }}>
                    Valid Input?
                  </text>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Stroke Weight & Line Quality */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          2. Stroke Weight & Line Quality
        </h2>
        <p
          style={{
            fontFamily: 'var(--pc-font-body)',
            fontSize: '16px',
            color: '#5a5a52',
            marginBottom: '24px'
          }}
        >
          All shapes use "normal pen" weight (2px) — confident and visible, like a real pen on paper.
        </p>

        <div className="mb-8">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
            Weight Comparison
          </h3>
          <svg width="800" height="120">
            {/* 0.5px - too thin */}
            <g>
              <path d={generateWobblyRect(150, 60, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="0.5" />
              <text x="75" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                0.5px
              </text>
              <text x="75" y="80" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Too thin
              </text>
            </g>

            {/* 1px - light pencil */}
            <g transform="translate(170, 0)">
              <path d={generateWobblyRect(150, 60, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1" />
              <text x="75" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                1px
              </text>
              <text x="75" y="80" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Light pencil
              </text>
            </g>

            {/* 2px - normal pen (chosen) */}
            <g transform="translate(340, 0)">
              <path d={generateWobblyRect(150, 60, 10)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="75" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-success-stroke)' }}>
                2px ✓
              </text>
              <text x="75" y="80" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: 'var(--pc-success-stroke)', fontWeight: 600 }}>
                Normal pen (default)
              </text>
            </g>

            {/* 3px - bold marker */}
            <g transform="translate(510, 0)">
              <path d={generateWobblyRect(150, 60, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="3" />
              <text x="75" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                3px
              </text>
              <text x="75" y="80" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Bold marker
              </text>
            </g>
          </svg>
        </div>

        <div>
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
            All Shape Types with Normal Pen Weight (2px)
          </h3>
          <div className="flex gap-6 flex-wrap">
            <svg width="120" height="80">
              <path d={generateWobblyRect(110, 70, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="55" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Rectangle
              </text>
            </svg>
            <svg width="80" height="80">
              <path d={generateWobblyRect(70, 70, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="35" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Square
              </text>
            </svg>
            <svg width="80" height="80">
              <path d={generateWobblyCircle(40, 40, 35)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="40" y="40" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Circle
              </text>
            </svg>
            <svg width="120" height="80">
              <path d={generateWobblyCircle(60, 40, 35)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="60" y="40" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Oval
              </text>
            </svg>
            <svg width="80" height="80">
              <path d={generateWobblyDiamond(70)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="35" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-neutral-stroke)' }}>
                Diamond
              </text>
            </svg>
          </div>
        </div>
      </section>

      {/* 3. Text Positioning & Justification */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          3. Text Positioning & Justification
        </h2>

        {/* Horizontal Alignment */}
        <div className="mb-12">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#5a5a52', marginBottom: '12px' }}>
            Horizontal Alignment
          </h3>
          <div className="flex gap-6">
            <svg width="200" height="110">
              <path d={generateWobblyRect(190, 100, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="20" y="35" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Deploy to
              </text>
              <text x="20" y="55" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Production
              </text>
              <text x="20" y="75" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Environment
              </text>
              <text x="95" y="115" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Left-aligned
              </text>
            </svg>

            <svg width="200" height="110">
              <path d={generateWobblyRect(190, 100, 10)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="95" y="35" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-success-stroke)' }}>
                Deploy to
              </text>
              <text x="95" y="55" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-success-stroke)' }}>
                Production
              </text>
              <text x="95" y="75" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-success-stroke)' }}>
                Environment
              </text>
              <text x="95" y="115" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: 'var(--pc-success-stroke)', fontWeight: 600 }}>
                Center (default)
              </text>
            </svg>

            <svg width="200" height="110">
              <path d={generateWobblyRect(190, 100, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="170" y="35" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Deploy to
              </text>
              <text x="170" y="55" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Production
              </text>
              <text x="170" y="75" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Environment
              </text>
              <text x="95" y="115" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Right-aligned
              </text>
            </svg>
          </div>
        </div>

        {/* Vertical Alignment */}
        <div className="mb-12">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#5a5a52', marginBottom: '12px' }}>
            Vertical Alignment
          </h3>
          <div className="flex gap-6">
            <svg width="140" height="160">
              <path d={generateWobblyRect(130, 150, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="65" y="25" textAnchor="middle" dominantBaseline="hanging"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Status
              </text>
              <text x="65" y="165" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Top
              </text>
            </svg>

            <svg width="140" height="160">
              <path d={generateWobblyRect(130, 150, 10)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="65" y="75" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-success-stroke)' }}>
                Status
              </text>
              <text x="65" y="165" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: 'var(--pc-success-stroke)', fontWeight: 600 }}>
                Middle (default)
              </text>
            </svg>

            <svg width="140" height="160">
              <path d={generateWobblyRect(130, 150, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="65" y="135" textAnchor="middle" dominantBaseline="baseline"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Status
              </text>
              <text x="65" y="165" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Bottom
              </text>
            </svg>
          </div>
        </div>

        {/* 3x3 Alignment Grid */}
        <div className="mb-8">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#5a5a52', marginBottom: '12px' }}>
            Complete 3×3 Alignment Matrix
          </h3>
          <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', color: '#5a5a52', marginBottom: '16px' }}>
            All 9 possible combinations — Middle-Center is the default
          </p>

          <div style={{ display: 'inline-block', border: '2px solid #ccc', borderRadius: '8px', padding: '16px', backgroundColor: 'white' }}>
            <table style={{ borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}></th>
                  <th style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Left</th>
                  <th style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Center</th>
                  <th style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Right</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Top</td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="10" y="18" textAnchor="start" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="10" y="32" textAnchor="start" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="45" y="18" textAnchor="middle" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="45" y="32" textAnchor="middle" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="80" y="18" textAnchor="end" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="80" y="32" textAnchor="end" dominantBaseline="hanging" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                </tr>
                <tr>
                  <td style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Middle</td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="10" y="28" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="10" y="42" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
                      <text x="45" y="28" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-success-stroke)' }}>Line 1</text>
                      <text x="45" y="42" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-success-stroke)' }}>Line 2</text>
                      <text x="45" y="88" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '9px', fill: 'var(--pc-success-stroke)', fontWeight: 600 }}>DEFAULT</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="80" y="28" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="80" y="42" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                </tr>
                <tr>
                  <td style={{ padding: '8px', fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888' }}>Bottom</td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="10" y="52" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="10" y="66" textAnchor="start" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="45" y="52" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="45" y="66" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                  <td style={{ padding: '4px' }}>
                    <svg width="100" height="80">
                      <path d={generateWobblyRect(90, 70, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
                      <text x="80" y="52" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 1</text>
                      <text x="80" y="66" textAnchor="end" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>Line 2</text>
                    </svg>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 4. Role-Based Visual Hierarchy */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          4. Role-Based Visual Hierarchy
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Text roles define visual importance through size and padding, not just font size.
        </p>

        <div className="flex gap-8 flex-wrap items-end">
          <div className="text-center">
            <svg width="300" height="100">
              <path d={generateWobblyRect(290, 90, 12)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2.5" />
              <text x="145" y="45" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-title)', fontSize: '32px', fill: 'var(--pc-highlight-stroke)', fontWeight: 700 }}>
                Hi
              </text>
            </svg>
            <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '8px' }}>
              <strong>Title</strong><br/>
              Min: 280×80px<br/>
              Padding: 1.8x<br/>
              Font: 32px bold
            </div>
          </div>

          <div className="text-center">
            <svg width="240" height="80">
              <path d={generateWobblyRect(230, 70, 10)} fill="var(--pc-info-fill)" stroke="var(--pc-info-stroke)" strokeWidth="2.5" />
              <text x="115" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-title)', fontSize: '24px', fill: 'var(--pc-info-stroke)', fontWeight: 600 }}>
                Hi
              </text>
            </svg>
            <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '8px' }}>
              <strong>Subtitle</strong><br/>
              Min: 220×60px<br/>
              Padding: 1.4x<br/>
              Font: 24px
            </div>
          </div>

          <div className="text-center">
            <svg width="80" height="60">
              <path d={generateWobblyRect(70, 50, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="35" y="25" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-neutral-stroke)' }}>
                Hi
              </text>
            </svg>
            <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '8px' }}>
              <strong>Body</strong><br/>
              No minimum<br/>
              Padding: 1.0x<br/>
              Font: 16px
            </div>
          </div>

          <div className="text-center">
            <svg width="70" height="50">
              <path d={generateWobblyRect(60, 40, 8)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="1.5" />
              <text x="30" y="20" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', fill: 'var(--pc-neutral-stroke)' }}>
                Hi
              </text>
            </svg>
            <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '8px' }}>
              <strong>Caption</strong><br/>
              No minimum<br/>
              Padding: 0.8x<br/>
              Font: 13px
            </div>
          </div>
        </div>
      </section>

      {/* 5. Grid Snapping & Spacing */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          5. Grid Snapping & Spacing
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Shapes snap to an invisible grid. Cell size: 160×120px with 24px margin.
        </p>

        <div className="mb-8">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
            Grid Layout Example
          </h3>
          <svg width="700" height="400">
            {/* Grid lines */}
            {[0, 1, 2, 3, 4].map(i => (
              <line key={`v${i}`} x1={i * 160} y1="0" x2={i * 160} y2="360"
                stroke="#ddd" strokeWidth="1" strokeDasharray="4,4" />
            ))}
            {[0, 1, 2, 3].map(i => (
              <line key={`h${i}`} x1="0" y1={i * 120} x2="640" y2={i * 120}
                stroke="#ddd" strokeWidth="1" strokeDasharray="4,4" />
            ))}

            {/* Shape 1 - normal */}
            <g transform="translate(12, 12)">
              <path d={generateWobblyRect(136, 96, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="68" y="48" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', fill: 'var(--pc-start-stroke)', fontWeight: 600 }}>
                1
              </text>
            </g>

            {/* Shape 2 */}
            <g transform="translate(172, 12)">
              <path d={generateWobblyRect(136, 96, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
              <text x="68" y="48" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', fill: 'var(--pc-highlight-stroke)', fontWeight: 600 }}>
                2
              </text>
            </g>

            {/* Shape 3 - spans 2 columns */}
            <g transform="translate(332, 12)">
              <path d={generateWobblyRect(296, 96, 10)} fill="var(--pc-info-fill)" stroke="var(--pc-info-stroke)" strokeWidth="2" />
              <text x="148" y="48" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', fill: 'var(--pc-info-stroke)', fontWeight: 600 }}>
                3 (spans 2 columns)
              </text>
            </g>

            {/* Shape 4 */}
            <g transform="translate(12, 132)">
              <path d={generateWobblyRect(136, 96, 10)} fill="var(--pc-decision-fill)" stroke="var(--pc-decision-stroke)" strokeWidth="2" />
              <text x="68" y="48" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', fill: 'var(--pc-decision-stroke)', fontWeight: 600 }}>
                4
              </text>
            </g>

            {/* Shape 5 */}
            <g transform="translate(172, 132)">
              <path d={generateWobblyRect(136, 96, 10)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="68" y="48" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', fill: 'var(--pc-success-stroke)', fontWeight: 600 }}>
                5
              </text>
            </g>

            {/* Annotations */}
            <text x="80" y="380" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', fill: '#888' }}>
              Cell: 160×120px
            </text>
            <text x="250" y="380" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', fill: '#888' }}>
              Margin: 24px between cells
            </text>
            <text x="450" y="380" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', fill: '#888' }}>
              Shapes snap to grid centers
            </text>
          </svg>
        </div>
      </section>

      {/* 6. Connector Attachment Points */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          6. Connector Attachment Points (9 Anchors)
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Every shape has 9 anchor points where connectors attach.
        </p>

        <div className="flex gap-12 flex-wrap">
          {/* Rectangle with anchors */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Rectangle Anchors
            </h3>
            <svg width="200" height="140">
              <path d={generateWobblyRect(180, 120, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />

              {/* Anchor points */}
              {[
                { x: 0, y: 0, label: 'TL' },
                { x: 90, y: 0, label: 'TC' },
                { x: 180, y: 0, label: 'TR' },
                { x: 0, y: 60, label: 'ML' },
                { x: 90, y: 60, label: 'MC' },
                { x: 180, y: 60, label: 'MR' },
                { x: 0, y: 120, label: 'BL' },
                { x: 90, y: 120, label: 'BC' },
                { x: 180, y: 120, label: 'BR' },
              ].map((anchor, i) => (
                <g key={i}>
                  <circle cx={anchor.x} cy={anchor.y} r="4" fill="#e74c3c" stroke="white" strokeWidth="1.5" />
                  <text x={anchor.x} y={anchor.y - 10} textAnchor="middle"
                    style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '10px', fill: '#e74c3c', fontWeight: 600 }}>
                    {anchor.label}
                  </text>
                </g>
              ))}
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '8px' }}>
              T=Top, M=Middle, B=Bottom<br/>
              L=Left, C=Center, R=Right
            </p>
          </div>

          {/* Circle with anchors */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Circle Anchors
            </h3>
            <svg width="140" height="140">
              <path d={generateWobblyCircle(70, 70, 60)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />

              {/* Anchor points on circle edge */}
              {[
                { x: 70, y: 10, label: 'TC' },
                { x: 130, y: 70, label: 'MR' },
                { x: 70, y: 130, label: 'BC' },
                { x: 10, y: 70, label: 'ML' },
                { x: 70, y: 70, label: 'MC' },
                { x: 112, y: 28, label: 'TR' },
                { x: 112, y: 112, label: 'BR' },
                { x: 28, y: 112, label: 'BL' },
                { x: 28, y: 28, label: 'TL' },
              ].map((anchor, i) => (
                <g key={i}>
                  <circle cx={anchor.x} cy={anchor.y} r="3" fill="#e74c3c" stroke="white" strokeWidth="1.5" />
                </g>
              ))}
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '8px' }}>
              Anchors map to shape edge<br/>
              (not bounding box)
            </p>
          </div>

          {/* Diamond with anchors */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Diamond Anchors
            </h3>
            <svg width="140" height="140">
              <g transform="translate(20, 20)">
                <path d={generateWobblyDiamond(100)} fill="var(--pc-decision-fill)" stroke="var(--pc-decision-stroke)" strokeWidth="2" />

                {/* Anchor points */}
                {[
                  { x: 50, y: 5, label: 'TC' },
                  { x: 95, y: 50, label: 'MR' },
                  { x: 50, y: 95, label: 'BC' },
                  { x: 5, y: 50, label: 'ML' },
                  { x: 50, y: 50, label: 'MC' },
                ].map((anchor, i) => (
                  <g key={i}>
                    <circle cx={anchor.x} cy={anchor.y} r="3" fill="#e74c3c" stroke="white" strokeWidth="1.5" />
                  </g>
                ))}
              </g>
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '8px' }}>
              Primary 5 anchors shown<br/>
              (4 corners map to edges)
            </p>
          </div>
        </div>
      </section>

      {/* 7. Connector Routing Styles */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          7. Connector Routing Styles
        </h2>

        <div className="mb-12">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#5a5a52', marginBottom: '16px' }}>
            Curved Connectors (Cubic Bezier)
          </h3>
          <svg width="700" height="180">
            {/* Horizontal S-curve */}
            <g>
              <path d={generateWobblyRect(80, 60, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="40" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-start-stroke)' }}>
                A
              </text>

              <path d={generateWobblyRect(80, 60, 10)} transform="translate(200, 0)" fill="var(--pc-end-fill)" stroke="var(--pc-end-stroke)" strokeWidth="2" />
              <text x="240" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-end-stroke)' }}>
                B
              </text>

              {/* Curved connector */}
              <path
                d="M 80 30 C 140 30, 140 30, 200 30"
                fill="none"
                stroke="var(--pc-neutral-stroke)"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path d="M 200 30 L 194 27 L 194 33 Z" fill="var(--pc-neutral-stroke)" />

              <text x="140" y="15" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Horizontal S-curve
              </text>
            </g>

            {/* Vertical curve */}
            <g transform="translate(350, 0)">
              <path d={generateWobblyRect(80, 60, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="40" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-start-stroke)' }}>
                C
              </text>

              <path d={generateWobblyRect(80, 60, 10)} transform="translate(0, 110)" fill="var(--pc-end-fill)" stroke="var(--pc-end-stroke)" strokeWidth="2" />
              <text x="40" y="140" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-end-stroke)' }}>
                D
              </text>

              {/* Vertical curved connector */}
              <path
                d="M 40 60 C 40 85, 40 85, 40 110"
                fill="none"
                stroke="var(--pc-neutral-stroke)"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path d="M 40 110 L 37 104 L 43 104 Z" fill="var(--pc-neutral-stroke)" />

              <text x="60" y="85" textAnchor="start" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Vertical<br/>curve
              </text>
            </g>
          </svg>
        </div>

        <div className="mb-12">
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#5a5a52', marginBottom: '16px' }}>
            Bent/Orthogonal Connectors (Right-Angle Routing)
          </h3>
          <svg width="700" height="200">
            {/* L-shaped route */}
            <g>
              <path d={generateWobblyRect(80, 60, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="40" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-start-stroke)' }}>
                A
              </text>

              <path d={generateWobblyRect(80, 60, 10)} transform="translate(200, 100)" fill="var(--pc-end-fill)" stroke="var(--pc-end-stroke)" strokeWidth="2" />
              <text x="240" y="130" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-end-stroke)' }}>
                B
              </text>

              {/* L-shaped bent connector with rounded corner */}
              <path
                d="M 80 30 L 140 30 Q 150 30, 150 40 L 150 100 Q 150 110, 160 110 L 200 110"
                fill="none"
                stroke="var(--pc-neutral-stroke)"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path d="M 200 110 L 194 107 L 194 113 Z" fill="var(--pc-neutral-stroke)" />

              <text x="140" y="15" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                L-shaped (one bend)
              </text>
            </g>

            {/* Z-shaped route */}
            <g transform="translate(350, 0)">
              <path d={generateWobblyRect(80, 60, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="40" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-start-stroke)' }}>
                C
              </text>

              <path d={generateWobblyRect(80, 60, 10)} transform="translate(200, 100)" fill="var(--pc-end-fill)" stroke="var(--pc-end-stroke)" strokeWidth="2" />
              <text x="240" y="130" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-end-stroke)' }}>
                D
              </text>

              {/* Z-shaped connector */}
              <path
                d="M 40 60 L 40 80 Q 40 90, 50 90 L 230 90 Q 240 90, 240 100 L 240 100"
                fill="none"
                stroke="var(--pc-neutral-stroke)"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path d="M 240 100 L 237 94 L 243 94 Z" fill="var(--pc-neutral-stroke)" />

              <text x="140" y="75" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
                Z-shaped (two bends)
              </text>
            </g>
          </svg>
        </div>
      </section>

      {/* 8. Connector Label Positioning */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          8. Connector Label Positioning
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Labels sit at the connector midpoint, offset perpendicular to avoid overlap.
        </p>

        <svg width="700" height="250">
          {/* Horizontal connector with label */}
          <g>
            <Connector x1={50} y1={50} x2={250} y2={50} arrow="forward" label="Yes" />
            <text x="150" y="90" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
              Horizontal connector
            </text>
          </g>

          {/* Diagonal connector with label */}
          <g transform="translate(0, 100)">
            <Connector x1={50} y1={30} x2={250} y2={100} arrow="forward" label="Maybe" />
            <text x="150" y="130" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
              Diagonal connector
            </text>
          </g>

          {/* Vertical connector with label */}
          <g transform="translate(350, 0)">
            <Connector x1={100} y1={30} x2={100} y2={200} arrow="forward" label="No" />
            <text x="100" y="230" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', fill: '#888' }}>
              Vertical connector
            </text>
          </g>
        </svg>
      </section>

      {/* 9. Boundary & Overlap Rules */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          9. Boundary & Overlap Rules — The Golden Rules
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          <strong>Critical layout constraints that prevent chaos</strong>
        </p>

        <div className="grid grid-cols-2 gap-8 mb-12">
          {/* Rule 1: No shape overlap */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
              ✓ Rule 1: No Shape Overlap
            </h3>
            <div className="flex gap-4">
              <div>
                <svg width="180" height="120">
                  {/* Incorrect - overlapping */}
                  <rect x="10" y="20" width="100" height="70" fill="none" stroke="red" strokeWidth="2" strokeDasharray="4,4" />
                  <rect x="60" y="20" width="100" height="70" fill="none" stroke="red" strokeWidth="2" strokeDasharray="4,4" />
                  <path d={generateWobblyRect(90, 60, 10)} transform="translate(15, 25)" fill="var(--pc-error-fill)" stroke="var(--pc-error-stroke)" strokeWidth="2" />
                  <path d={generateWobblyRect(90, 60, 10)} transform="translate(65, 25)" fill="var(--pc-error-fill)" stroke="var(--pc-error-stroke)" strokeWidth="2" />
                  <text x="90" y="110" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', fill: 'red' }}>✗</text>
                </svg>
                <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: 'red', textAlign: 'center' }}>
                  Incorrect<br/>Bounding boxes overlap
                </p>
              </div>

              <div>
                <svg width="220" height="120">
                  {/* Correct - clear spacing */}
                  <rect x="10" y="20" width="80" height="70" fill="none" stroke="green" strokeWidth="2" strokeDasharray="4,4" />
                  <rect x="120" y="20" width="80" height="70" fill="none" stroke="green" strokeWidth="2" strokeDasharray="4,4" />
                  <path d={generateWobblyRect(70, 60, 10)} transform="translate(15, 25)" fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
                  <path d={generateWobblyRect(70, 60, 10)} transform="translate(125, 25)" fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
                  <text x="110" y="110" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', fill: 'green' }}>✓</text>
                </svg>
                <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: 'green', textAlign: 'center' }}>
                  Correct<br/>Clear spacing
                </p>
              </div>
            </div>
          </div>

          {/* Rule 2: No shape-text overlap */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
              ✓ Rule 2: No Shape-Text Overlap
            </h3>
            <svg width="250" height="120">
              <rect x="120" y="20" width="110" height="40" fill="none" stroke="green" strokeWidth="1" strokeDasharray="3,3" opacity="0.5" />
              <text x="175" y="35" textAnchor="middle" dominantBaseline="hanging"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-neutral-stroke)' }}>
                Free text label
              </text>

              <rect x="15" y="55" width="90" height="50" fill="none" stroke="green" strokeWidth="2" strokeDasharray="4,4" />
              <path d={generateWobblyRect(80, 40, 10)} transform="translate(20, 60)" fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="60" y="80" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-success-stroke)' }}>
                Shape
              </text>
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: 'green', marginTop: '8px' }}>
              Text and shape bounding boxes don't overlap
            </p>
          </div>

          {/* Rule 3: Connectors may cross margins */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
              ✓ Rule 3: Connectors May Cross Margins
            </h3>
            <svg width="300" height="150">
              {/* Shape with bounding box */}
              <rect x="100" y="35" width="100" height="80" fill="none" stroke="#ccc" strokeWidth="2" strokeDasharray="4,4" opacity="0.5" />
              <path d={generateWobblyRect(80, 60, 10)} transform="translate(110, 45)" fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />

              {/* Connector passing through margin (allowed) */}
              <path d="M 30 75 L 220 75" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <path d="M 220 75 L 214 72 L 214 78 Z" fill="var(--pc-neutral-stroke)" />

              <text x="150" y="130" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: 'green' }}>
                ✓ Connector can cross margin area<br/>(but curves around visible shape)
              </text>
            </svg>
          </div>

          {/* Rule 4: Connectors may cross each other */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '12px' }}>
              ✓ Rule 4: Connectors May Cross
            </h3>
            <svg width="250" height="150">
              <path d="M 30 50 L 220 50" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <path d="M 220 50 L 214 47 L 214 53 Z" fill="var(--pc-neutral-stroke)" />

              <path d="M 125 20 L 125 110" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
              <path d="M 125 110 L 122 104 L 128 104 Z" fill="var(--pc-highlight-stroke)" />

              <circle cx="125" cy="50" r="3" fill="white" stroke="var(--pc-neutral-stroke)" strokeWidth="1" />

              <text x="125" y="135" textAnchor="middle" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: 'green' }}>
                ✓ Connector crossing is OK
              </text>
            </svg>
          </div>
        </div>

        {/* Summary diagram */}
        <div>
          <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '20px', color: '#2a2a24', marginBottom: '16px' }}>
            All Rules Together — Layout Example
          </h3>
          <svg width="700" height="350">
            {/* Background grid hint */}
            {[0, 1, 2, 3, 4].map(i => (
              <line key={`vg${i}`} x1={i * 160} y1="0" x2={i * 160} y2="320"
                stroke="#f0f0f0" strokeWidth="1" strokeDasharray="4,4" />
            ))}
            {[0, 1, 2].map(i => (
              <line key={`hg${i}`} x1="0" y1={i * 160} x2="640" y2={i * 160}
                stroke="#f0f0f0" strokeWidth="1" strokeDasharray="4,4" />
            ))}

            {/* Shape 1 */}
            <g transform="translate(20, 20)">
              <rect x="-5" y="-5" width="110" height="80" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <path d={generateWobblyRect(100, 70, 10)} fill="var(--pc-start-fill)" stroke="var(--pc-start-stroke)" strokeWidth="2" />
              <text x="50" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', fill: 'var(--pc-start-stroke)' }}>
                Start
              </text>
            </g>

            {/* Shape 2 */}
            <g transform="translate(200, 30)">
              <rect x="-5" y="-5" width="110" height="70" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
              <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-highlight-stroke)' }}>
                Process
              </text>
            </g>

            {/* Shape 3 - Diamond */}
            <g transform="translate(400, 10)">
              <rect x="-5" y="-5" width="90" height="90" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <path d={generateWobblyDiamond(80)} fill="var(--pc-decision-fill)" stroke="var(--pc-decision-stroke)" strokeWidth="2" />
              <text x="40" y="40" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '12px', fill: 'var(--pc-decision-stroke)' }}>
                Valid?
              </text>
            </g>

            {/* Shape 4 */}
            <g transform="translate(30, 180)">
              <rect x="-5" y="-5" width="100" height="70" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <path d={generateWobblyRect(90, 60, 10)} fill="var(--pc-error-fill)" stroke="var(--pc-error-stroke)" strokeWidth="2" />
              <text x="45" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-error-stroke)' }}>
                Error
              </text>
            </g>

            {/* Shape 5 */}
            <g transform="translate(520, 180)">
              <rect x="-5" y="-5" width="100" height="70" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <path d={generateWobblyCircle(45, 30, 30)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
              <text x="45" y="30" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-success-stroke)' }}>
                Done
              </text>
            </g>

            {/* Free text */}
            <g transform="translate(180, 150)">
              <rect x="-3" y="-3" width="86" height="26" fill="none" stroke="#ccc" strokeWidth="1" strokeDasharray="2,2" opacity="0.4" />
              <text x="40" y="10" textAnchor="middle" dominantBaseline="hanging"
                style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', fill: '#5a5a52' }}>
                annotation
              </text>
            </g>

            {/* Connectors */}
            <Connector x1={120} y1={55} x2={200} y2={60} arrow="forward" />
            <Connector x1={300} y1={60} x2={400} y2={55} arrow="forward" />
            <Connector x1={440} y1={90} x2={565} y2={180} arrow="forward" label="Yes" />
            <Connector x1={420} y1={55} x2={180} y2={210} arrow="forward" style="dashed" label="No" />
            <Connector x1={120} y1={210} x2={520} y2={210} arrow="none" style="dashed" />
          </svg>
          <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#5a5a52', marginTop: '12px', fontStyle: 'italic' }}>
            Dotted outlines show bounding boxes. Note: Clear gaps between all shapes, connectors route around (not through) shapes, connectors can cross each other.
          </p>
        </div>
      </section>

      {/* 10. Section Container Behavior */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          10. Section Container Behavior
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Sections dynamically size around contained shapes with padding. Label stays top-left.
        </p>

        <div className="flex gap-8 flex-wrap">
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#888', marginBottom: '8px' }}>
              2 shapes
            </h3>
            <svg width="280" height="180">
              {/* Section background */}
              <path d={generateWobblyRect(270, 170, 14)} fill="rgba(204, 221, 255, 0.2)" stroke="rgba(107, 143, 204, 0.4)" strokeWidth="2" strokeDasharray="5,5" />
              <text x="15" y="20" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', fill: 'rgba(107, 143, 204, 0.8)' }}>
                Validation
              </text>

              {/* Shapes inside */}
              <g transform="translate(20, 40)">
                <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
                <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-highlight-stroke)' }}>
                  Check
                </text>
              </g>
              <g transform="translate(140, 40)">
                <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
                <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-highlight-stroke)' }}>
                  Verify
                </text>
              </g>
            </svg>
          </div>

          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#888', marginBottom: '8px' }}>
              3 shapes (section grows)
            </h3>
            <svg width="280" height="240">
              {/* Larger section background */}
              <path d={generateWobblyRect(270, 230, 14)} fill="rgba(204, 221, 255, 0.2)" stroke="rgba(107, 143, 204, 0.4)" strokeWidth="2" strokeDasharray="5,5" />
              <text x="15" y="20" style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', fill: 'rgba(107, 143, 204, 0.8)' }}>
                Validation
              </text>

              {/* Shapes inside */}
              <g transform="translate(20, 40)">
                <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
                <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-highlight-stroke)' }}>
                  Check
                </text>
              </g>
              <g transform="translate(140, 40)">
                <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-highlight-fill)" stroke="var(--pc-highlight-stroke)" strokeWidth="2" />
                <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-highlight-stroke)' }}>
                  Verify
                </text>
              </g>
              <g transform="translate(80, 120)">
                <path d={generateWobblyRect(100, 60, 10)} fill="var(--pc-success-fill)" stroke="var(--pc-success-stroke)" strokeWidth="2" />
                <text x="50" y="30" textAnchor="middle" dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '13px', fill: 'var(--pc-success-stroke)' }}>
                  Confirm
                </text>
              </g>
            </svg>
          </div>
        </div>

        <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888', marginTop: '16px' }}>
          Z-order: Section backgrounds render behind connectors, which render behind shapes
        </p>
      </section>

      {/* 11. Edge Cases */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          11. Edge Cases
        </h2>

        <div className="grid grid-cols-3 gap-6">
          {/* Empty text */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Empty Text
            </h3>
            <svg width="100" height="80">
              <path d={generateWobblyRect(90, 70, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '4px' }}>
              Still has minimum size<br/>No visible text
            </p>
          </div>

          {/* Very long word */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Very Long Word
            </h3>
            <svg width="220" height="80">
              <path d={generateWobblyRect(210, 70, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              <text x="105" y="35" textAnchor="middle" dominantBaseline="middle"
                style={{ fontFamily: 'var(--pc-font-body)', fontSize: '11px', fill: 'var(--pc-neutral-stroke)' }}>
                Supercalifragilistic...
              </text>
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '4px' }}>
              Stretches wide<br/>Single-line overflow
            </p>
          </div>

          {/* Many lines */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '12px' }}>
              Many Lines
            </h3>
            <svg width="180" height="160">
              <path d={generateWobblyRect(170, 150, 10)} fill="var(--pc-neutral-fill)" stroke="var(--pc-neutral-stroke)" strokeWidth="2" />
              {[0, 1, 2, 3, 4, 5].map(i => (
                <text key={i} x="85" y={30 + i * 20} textAnchor="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '12px', fill: 'var(--pc-neutral-stroke)' }}>
                  Line {i + 1}
                </text>
              ))}
            </svg>
            <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '11px', color: '#888', marginTop: '4px' }}>
              Grows tall<br/>Wrapped content
            </p>
          </div>
        </div>
      </section>

      {/* 12. Component Library Reference */}
      <section className="mb-16">
        <h2
          style={{
            fontFamily: 'var(--pc-font-title)',
            fontSize: '36px',
            color: '#2a2a24',
            marginBottom: '24px',
            fontWeight: 600
          }}
        >
          12. Implementation Component Library
        </h2>
        <p style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', color: '#5a5a52', marginBottom: '24px' }}>
          Quick-reference toolbox for building diagrams
        </p>

        <div
          style={{
            backgroundColor: 'white',
            border: '3px solid var(--pc-neutral-stroke)',
            borderRadius: '16px',
            padding: '32px'
          }}
        >
          {/* Shape components */}
          <div className="mb-12">
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '16px' }}>
              Shape Types (Neutral)
            </h3>
            <div className="flex gap-6 flex-wrap items-center">
              {[
                { shape: 'rectangle', label: 'Rectangle' },
                { shape: 'square', label: 'Square' },
                { shape: 'circle', label: 'Circle' },
                { shape: 'oval', label: 'Oval' },
                { shape: 'diamond', label: 'Diamond' },
                { shape: 'text', label: 'Free Text' }
              ].map((item, i) => (
                <div key={i} className="text-center">
                  <ShapeBox theme={colorThemes[0]} shape={item.shape as any} label={item.label} size="sm" />
                </div>
              ))}
            </div>
          </div>

          {/* Color themes */}
          <div className="mb-12">
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '16px' }}>
              Color Themes
            </h3>
            <div className="flex gap-3 flex-wrap">
              {colorThemes.map((theme, i) => (
                <ShapeBox key={i} theme={theme} shape="rectangle" label={theme.name} size="sm" />
              ))}
            </div>
          </div>

          {/* Connector styles */}
          <div className="mb-12">
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '16px' }}>
              Connector Styles
            </h3>
            <div className="space-y-4">
              <div>
                <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                  Line Styles
                </p>
                <svg width="600" height="50">
                  <Connector x1={20} y1={20} x2={170} y2={20} style="solid" arrow="forward" label="Solid" />
                  <Connector x1={220} y1={20} x2={370} y2={20} style="dashed" arrow="forward" label="Dashed" />
                  <Connector x1={420} y1={20} x2={570} y2={20} style="dotted" arrow="forward" label="Dotted" />
                </svg>
              </div>

              <div>
                <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                  Line Weights
                </p>
                <svg width="600" height="50">
                  <Connector x1={20} y1={20} x2={170} y2={20} weight="thin" arrow="forward" label="Thin" />
                  <Connector x1={220} y1={20} x2={370} y2={20} weight="normal" arrow="forward" label="Normal" />
                  <Connector x1={420} y1={20} x2={570} y2={20} weight="bold" arrow="forward" label="Bold" />
                </svg>
              </div>

              <div>
                <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                  Arrow Types
                </p>
                <svg width="700" height="50">
                  <Connector x1={20} y1={20} x2={140} y2={20} arrow="forward" label="Forward" />
                  <Connector x1={180} y1={20} x2={300} y2={20} arrow="backward" label="Back" />
                  <Connector x1={340} y1={20} x2={460} y2={20} arrow="both" label="Both" />
                  <Connector x1={500} y1={20} x2={620} y2={20} arrow="none" label="None" />
                </svg>
              </div>
            </div>
          </div>

          {/* Boundary rules cheat sheet */}
          <div>
            <h3 style={{ fontFamily: 'var(--pc-font-body)', fontSize: '18px', color: '#5a5a52', marginBottom: '16px' }}>
              Golden Rules Cheat Sheet
            </h3>
            <div
              style={{
                backgroundColor: 'var(--pc-warning-fill)',
                border: '2px solid var(--pc-warning-stroke)',
                borderRadius: '8px',
                padding: '16px'
              }}
            >
              <ul style={{ fontFamily: 'var(--pc-font-body)', fontSize: '14px', color: 'var(--pc-warning-stroke)', lineHeight: '1.8' }}>
                <li>✓ No shape may overlap any other shape</li>
                <li>✓ No shape may overlap any text</li>
                <li>✓ Connectors may cross bounding box margins</li>
                <li>✓ Connectors may cross each other</li>
                <li>✓ All shapes snap to grid (160×120px cells, 24px margin)</li>
                <li>✓ Default stroke: 2px ("normal pen")</li>
                <li>✓ Default alignment: middle-center</li>
                <li>✓ Minimum shape padding: 16px</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'visual' | 'behavior'>('visual');

  return (
    <div className="min-h-screen p-8 overflow-auto" style={{ backgroundColor: '#fdf6e3' }}>
      <div className="max-w-[1600px] mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '56px',
              color: '#2a2a24',
              marginBottom: '8px',
              fontWeight: 700
            }}
          >
            PlotCraft Design System
          </h1>
          <p
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '22px',
              color: '#5a5a52',
              marginBottom: '24px'
            }}
          >
            Hand-drawn, sketchy, warm — like your favorite whiteboard
          </p>

          {/* Tab Switcher */}
          <div className="flex justify-center gap-4 mt-8">
            <button
              onClick={() => setActiveTab('visual')}
              style={{
                fontFamily: 'var(--pc-font-body)',
                fontSize: '18px',
                padding: '12px 32px',
                backgroundColor: activeTab === 'visual' ? 'var(--pc-highlight-fill)' : 'transparent',
                border: `2px solid ${activeTab === 'visual' ? 'var(--pc-highlight-stroke)' : '#ddd'}`,
                borderRadius: '8px',
                color: activeTab === 'visual' ? 'var(--pc-highlight-stroke)' : '#5a5a52',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              Visual Style
            </button>
            <button
              onClick={() => setActiveTab('behavior')}
              style={{
                fontFamily: 'var(--pc-font-body)',
                fontSize: '18px',
                padding: '12px 32px',
                backgroundColor: activeTab === 'behavior' ? 'var(--pc-highlight-fill)' : 'transparent',
                border: `2px solid ${activeTab === 'behavior' ? 'var(--pc-highlight-stroke)' : '#ddd'}`,
                borderRadius: '8px',
                color: activeTab === 'behavior' ? 'var(--pc-highlight-stroke)' : '#5a5a52',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              Dynamic Behavior
            </button>
          </div>
        </div>

        {activeTab === 'visual' && (
          <>
        {/* 1. Color Palette */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            1. Color Palette — 9 Semantic Themes
          </h2>
          <div className="flex flex-wrap gap-6">
            {colorThemes.map((theme) => (
              <div key={theme.name} className="text-center">
                <ShapeBox theme={theme} label={theme.name} />
                <div
                  style={{
                    fontFamily: 'var(--pc-font-caption)',
                    fontSize: '14px',
                    color: '#5a5a52',
                    marginTop: '8px'
                  }}
                >
                  {theme.name}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 2. Shape Library */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            2. Shape Library — 6 Types
          </h2>
          <div className="mb-8">
            <h3
              style={{
                fontFamily: 'var(--pc-font-body)',
                fontSize: '20px',
                color: '#5a5a52',
                marginBottom: '16px'
              }}
            >
              Basic Shapes (Neutral)
            </h3>
            <div className="flex flex-wrap gap-6 items-center">
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="rectangle" label="Rectangle" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Rectangle
                </div>
              </div>
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="square" label="Square" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Square
                </div>
              </div>
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="circle" label="Circle" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Circle
                </div>
              </div>
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="oval" label="Oval" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Oval
                </div>
              </div>
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="diamond" label="Diamond" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Diamond
                </div>
              </div>
              <div className="text-center">
                <ShapeBox theme={colorThemes[0]} shape="text" label="Free Text" size="md" />
                <div style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '12px', marginTop: '4px' }}>
                  Text Only
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3
              style={{
                fontFamily: 'var(--pc-font-body)',
                fontSize: '20px',
                color: '#5a5a52',
                marginBottom: '16px'
              }}
            >
              Rectangle in All Color Themes
            </h3>
            <div className="flex flex-wrap gap-4">
              {colorThemes.map((theme) => (
                <ShapeBox key={theme.name} theme={theme} shape="rectangle" label={theme.name} size="sm" />
              ))}
            </div>
          </div>
        </section>

        {/* 3. Typography Scale */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            3. Typography Scale — 4 Levels
          </h2>

          <div className="space-y-8">
            {/* Title */}
            <div>
              <div
                style={{
                  fontFamily: 'var(--pc-font-title)',
                  fontSize: '48px',
                  color: '#2a2a24',
                  fontWeight: 700,
                  marginBottom: '8px'
                }}
              >
                Title — Whiteboard Header
              </div>
              <div className="mt-4">
                <ShapeBox
                  theme={colorThemes[0]}
                  shape="rectangle"
                  label="Title Inside Shape"
                  size="lg"
                />
              </div>
              <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#5a5a52', marginTop: '8px' }}>
                Font: Caveat Bold, 48px — Like a thick marker header
              </p>
            </div>

            {/* Subtitle */}
            <div>
              <div
                style={{
                  fontFamily: 'var(--pc-font-title)',
                  fontSize: '32px',
                  color: '#2a2a24',
                  fontWeight: 600,
                  marginBottom: '8px'
                }}
              >
                Subtitle — Section Label
              </div>
              <div className="mt-4">
                <ShapeBox
                  theme={colorThemes[0]}
                  shape="rectangle"
                  label="Subtitle Text"
                  size="md"
                />
              </div>
              <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#5a5a52', marginTop: '8px' }}>
                Font: Caveat Semi-Bold, 32px — Section headers
              </p>
            </div>

            {/* Body */}
            <div>
              <div
                style={{
                  fontFamily: 'var(--pc-font-body)',
                  fontSize: '18px',
                  color: '#2a2a24',
                  marginBottom: '8px'
                }}
              >
                Body — Standard node text, comfortable reading size
              </div>
              <div className="mt-4">
                <ShapeBox
                  theme={colorThemes[0]}
                  shape="rectangle"
                  label="Body Text Here"
                  size="md"
                />
              </div>
              <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#5a5a52', marginTop: '8px' }}>
                Font: Patrick Hand, 18px — Default node text
              </p>
            </div>

            {/* Caption */}
            <div>
              <div
                style={{
                  fontFamily: 'var(--pc-font-caption)',
                  fontSize: '14px',
                  color: '#5a5a52',
                  marginBottom: '8px'
                }}
              >
                Caption — Small annotations, like pencil notes in the margin
              </div>
              <div className="mt-4">
                <ShapeBox
                  theme={colorThemes[0]}
                  shape="rectangle"
                  label="Small Note"
                  size="sm"
                />
              </div>
              <p style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', color: '#5a5a52', marginTop: '8px' }}>
                Font: Indie Flower, 14px — Annotations and labels
              </p>
            </div>
          </div>
        </section>

        {/* 4. Connectors & Arrows */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            4. Connectors & Arrows
          </h2>

          <div className="space-y-8">
            {/* Line Styles */}
            <div>
              <h3
                style={{
                  fontFamily: 'var(--pc-font-body)',
                  fontSize: '20px',
                  color: '#5a5a52',
                  marginBottom: '16px'
                }}
              >
                Line Styles
              </h3>
              <svg width="700" height="150">
                <Connector x1={50} y1={30} x2={300} y2={30} style="solid" arrow="forward" label="Solid Line" />
                <Connector x1={50} y1={70} x2={300} y2={70} style="dashed" arrow="forward" label="Dashed Line" />
                <Connector x1={50} y1={110} x2={300} y2={110} style="dotted" arrow="forward" label="Dotted Line" />
              </svg>
            </div>

            {/* Line Weights */}
            <div>
              <h3
                style={{
                  fontFamily: 'var(--pc-font-body)',
                  fontSize: '20px',
                  color: '#5a5a52',
                  marginBottom: '16px'
                }}
              >
                Line Weights
              </h3>
              <svg width="700" height="150">
                <Connector x1={50} y1={30} x2={300} y2={30} weight="thin" arrow="forward" label="Thin (pencil)" />
                <Connector x1={50} y1={70} x2={300} y2={70} weight="normal" arrow="forward" label="Normal (pen)" />
                <Connector x1={50} y1={110} x2={300} y2={110} weight="bold" arrow="forward" label="Bold (marker)" />
              </svg>
            </div>

            {/* Arrow Types */}
            <div>
              <h3
                style={{
                  fontFamily: 'var(--pc-font-body)',
                  fontSize: '20px',
                  color: '#5a5a52',
                  marginBottom: '16px'
                }}
              >
                Arrow Types
              </h3>
              <svg width="700" height="180">
                <Connector x1={50} y1={30} x2={300} y2={30} arrow="forward" label="Forward" />
                <Connector x1={50} y1={70} x2={300} y2={70} arrow="backward" label="Backward" />
                <Connector x1={50} y1={110} x2={300} y2={110} arrow="both" label="Bidirectional" />
                <Connector x1={50} y1={150} x2={300} y2={150} arrow="none" label="No Arrow" />
              </svg>
            </div>
          </div>
        </section>

        {/* 5. Section Grouping */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            5. Section Grouping
          </h2>
          <p
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '16px',
              color: '#5a5a52',
              marginBottom: '24px'
            }}
          >
            Loose boundaries around groups — like "this area of the whiteboard"
          </p>

          <div className="flex flex-wrap gap-8">
            <SectionBox title="Neutral Section" color="neutral">
              <div className="flex gap-4 flex-wrap">
                <ShapeBox theme={colorThemes[0]} shape="rectangle" label="Item 1" size="sm" />
                <ShapeBox theme={colorThemes[0]} shape="circle" label="Item 2" size="sm" />
              </div>
            </SectionBox>

            <SectionBox title="Highlight Section" color="highlight">
              <div className="flex gap-4 flex-wrap">
                <ShapeBox theme={colorThemes[5]} shape="rectangle" label="Important" size="sm" />
                <ShapeBox theme={colorThemes[5]} shape="square" label="Note" size="sm" />
              </div>
            </SectionBox>

            <SectionBox title="Info Section" color="info">
              <div className="flex gap-4 flex-wrap">
                <ShapeBox theme={colorThemes[6]} shape="oval" label="Detail" size="sm" />
                <ShapeBox theme={colorThemes[6]} shape="rectangle" label="Info" size="sm" />
              </div>
            </SectionBox>
          </div>
        </section>

        {/* 6. Reference Composition */}
        <section className="mb-16">
          <h2
            style={{
              fontFamily: 'var(--pc-font-title)',
              fontSize: '36px',
              color: '#2a2a24',
              marginBottom: '24px',
              fontWeight: 600
            }}
          >
            6. Reference Composition — Complete Example
          </h2>
          <p
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '16px',
              color: '#5a5a52',
              marginBottom: '32px'
            }}
          >
            A well-done whiteboard sketch — the kind you'd photograph and share with your team
          </p>

          <div className="relative bg-white/30 p-8 rounded-lg" style={{
            border: '2px dashed rgba(90, 90, 82, 0.2)',
            minHeight: '700px'
          }}>
            <div
              style={{
                fontFamily: 'var(--pc-font-title)',
                fontSize: '42px',
                color: '#2a2a24',
                fontWeight: 700,
                marginBottom: '32px',
                textAlign: 'center'
              }}
            >
              User Registration Flow
            </div>

            {/* SVG Canvas for the flowchart */}
            <svg width="900" height="600" style={{ display: 'block', margin: '0 auto' }}>
              {/* Start Node */}
              <g>
                <path
                  d={generateWobblyCircle(100, 80, 50)}
                  fill="var(--pc-start-fill)"
                  stroke="var(--pc-start-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="100"
                  y="80"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-start-stroke)' }}
                >
                  Start
                </text>
              </g>

              {/* Connector to Form */}
              <Connector x1={150} y1={80} x2={220} y2={80} arrow="forward" />

              {/* Form Input */}
              <g>
                <path
                  d={generateWobblyRect(180, 90, 12)}
                  transform="translate(230, 35)"
                  fill="var(--pc-highlight-fill)"
                  stroke="var(--pc-highlight-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="320"
                  y="80"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-highlight-stroke)' }}
                >
                  Enter Email &
                </text>
                <text
                  x="320"
                  y="95"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-highlight-stroke)' }}
                >
                  Password
                </text>
              </g>

              {/* Connector to Validation */}
              <Connector x1={410} y1={80} x2={480} y2={80} arrow="forward" />

              {/* Validation Decision */}
              <g>
                <path
                  d={generateWobblyDiamond(110)}
                  transform="translate(480, 25)"
                  fill="var(--pc-decision-fill)"
                  stroke="var(--pc-decision-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="535"
                  y="75"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-decision-stroke)' }}
                >
                  Valid?
                </text>
              </g>

              {/* No path - Error */}
              <Connector x1={535} y1={135} x2={535} y2={200} arrow="forward" label="No" />

              {/* Error Node */}
              <g>
                <path
                  d={generateWobblyRect(160, 80, 12)}
                  transform="translate(455, 210)"
                  fill="var(--pc-error-fill)"
                  stroke="var(--pc-error-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="535"
                  y="245"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-error-stroke)' }}
                >
                  Show Error
                </text>
                <text
                  x="535"
                  y="260"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-error-stroke)' }}
                >
                  Message
                </text>
              </g>

              {/* Loop back to form */}
              <Connector x1={455} y1={250} x2={320} y2={250} arrow="none" style="dashed" />
              <Connector x1={320} y1={250} x2={320} y2={125} arrow="forward" style="dashed" />

              {/* Yes path - Create Account */}
              <Connector x1={590} y1={80} x2={660} y2={80} arrow="forward" label="Yes" />

              {/* Create Account */}
              <g>
                <path
                  d={generateWobblyRect(180, 90, 12)}
                  transform="translate(670, 35)"
                  fill="var(--pc-info-fill)"
                  stroke="var(--pc-info-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="760"
                  y="75"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-info-stroke)' }}
                >
                  Create Account
                </text>
                <text
                  x="760"
                  y="90"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-info-stroke)' }}
                >
                  in Database
                </text>
              </g>

              {/* Connector to Send Email */}
              <Connector x1={760} y1={125} x2={760} y2={190} arrow="forward" />

              {/* Send Email */}
              <g>
                <path
                  d={generateWobblyRect(180, 90, 12)}
                  transform="translate(670, 200)"
                  fill="var(--pc-warning-fill)"
                  stroke="var(--pc-warning-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="760"
                  y="240"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-warning-stroke)' }}
                >
                  Send Welcome
                </text>
                <text
                  x="760"
                  y="255"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '15px', fill: 'var(--pc-warning-stroke)' }}
                >
                  Email
                </text>
              </g>

              {/* Connector to Success */}
              <Connector x1={760} y1={290} x2={760} y2={360} arrow="forward" />

              {/* Success/End */}
              <g>
                <path
                  d={generateWobblyCircle(760, 410, 50)}
                  fill="var(--pc-success-fill)"
                  stroke="var(--pc-success-stroke)"
                  strokeWidth="2.5"
                />
                <text
                  x="760"
                  y="410"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  style={{ fontFamily: 'var(--pc-font-body)', fontSize: '16px', fill: 'var(--pc-success-stroke)' }}
                >
                  Success!
                </text>
              </g>

              {/* Section: Validation Area */}
              <g opacity="0.6">
                <path
                  d={generateWobblyRect(250, 200, 16)}
                  transform="translate(430, 10)"
                  fill="rgba(204, 221, 255, 0.15)"
                  stroke="rgba(107, 143, 204, 0.3)"
                  strokeWidth="2"
                  strokeDasharray="6,4"
                />
                <text
                  x="440"
                  y="30"
                  style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', fill: 'rgba(107, 143, 204, 0.8)' }}
                >
                  Validation Step
                </text>
              </g>

              {/* Section: Database Operations */}
              <g opacity="0.6">
                <path
                  d={generateWobblyRect(220, 280, 16)}
                  transform="translate(650, 20)"
                  fill="rgba(178, 236, 227, 0.12)"
                  stroke="rgba(77, 170, 154, 0.3)"
                  strokeWidth="2"
                  strokeDasharray="6,4"
                />
                <text
                  x="660"
                  y="40"
                  style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '14px', fill: 'rgba(77, 170, 154, 0.8)' }}
                >
                  Database & Email
                </text>
              </g>

              {/* Annotations */}
              <text
                x="100"
                y="150"
                style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', fill: '#5a5a52' }}
              >
                User initiates
              </text>
              <text
                x="650"
                y="480"
                style={{ fontFamily: 'var(--pc-font-caption)', fontSize: '13px', fill: '#5a5a52' }}
              >
                ✓ Account created
              </text>
            </svg>
          </div>
        </section>

          </>
        )}

        {activeTab === 'behavior' && (
          <>
            {/* Behavior sections will go here */}
            <BehaviorSections />
          </>
        )}

        {/* Footer */}
        <div className="text-center mt-16 pb-8">
          <p
            style={{
              fontFamily: 'var(--pc-font-body)',
              fontSize: '16px',
              color: '#5a5a52',
            }}
          >
            Hand-drawn with care • PlotCraft Design System • {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </div>
  );
}
