"""
Holaho - Modern Glassmorphism QSS Stylesheet
Vibrant violet, magenta & dark slate aesthetic with glowing accents.
"""

HOLAHO_STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #0d0e1b;
    color: #f1f5f9;
    font-family: 'Segoe UI', Inter, sans-serif;
    font-size: 13px;
}

#HolahoWidget {
    background-color: rgba(18, 16, 38, 0.94);
    border: 1px solid rgba(168, 85, 247, 0.45);
    border-radius: 22px;
}

#WidgetTitle {
    color: #c084fc;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 0.5px;
}

/* Buttons */
QPushButton {
    background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%);
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 7px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: linear-gradient(135deg, #8b5cf6 0%, #d8b4fe 100%);
}

QPushButton:pressed {
    background-color: #6d28d9;
}

QPushButton#RecordBtn {
    background: linear-gradient(135deg, #ec4899 0%, #ef4444 100%);
    font-weight: bold;
    border-radius: 12px;
}

QPushButton#RecordBtn:hover {
    background: linear-gradient(135deg, #f472b6 0%, #f87171 100%);
}

QPushButton#MediaBtn {
    background-color: #1e1b4b;
    border: 1px solid #3730a3;
    border-radius: 8px;
    color: #a5b4fc;
}

QPushButton#MediaBtn:hover {
    background-color: #312e81;
    color: #ffffff;
}

/* Controls */
QLineEdit, QSpinBox, QComboBox {
    background-color: #1e1e38;
    border: 1px solid #383868;
    border-radius: 6px;
    color: #f8fafc;
    padding: 6px 10px;
}

QListWidget {
    background-color: #13132b;
    border: 1px solid #2d2b55;
    border-radius: 8px;
    color: #e2e8f0;
    padding: 4px;
}

QListWidget::item:selected {
    background-color: #4c1d95;
    color: #ffffff;
    border-radius: 4px;
}
"""
