import sys
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QProgressBar,
    QFrame
)


class SJFWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIXEL CPU // SJF SIMULATOR")
        self.resize(1000, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #101820;
                color: #d9f99d;
                font-family: "Courier New";
                font-size: 14px;
            }

            QLabel {
                color: #d9f99d;
            }

            QLineEdit {
                background-color: #17232d;
                border: 2px solid #3b5c46;
                padding: 10px;
                color: #d9f99d;
                font-family: "Courier New";
                font-weight: bold;
            }

            QLineEdit:focus {
                border: 2px solid #9cff57;
            }

            QPushButton {
                background-color: #1c3325;
                border: 2px solid #5c9142;
                color: #b9ff72;
                padding: 10px 16px;
                font-family: "Courier New";
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2b4d32;
                border: 2px solid #b9ff72;
            }

            QPushButton:pressed {
                background-color: #416b42;
            }

            QTableWidget {
                background-color: #111a20;
                border: 2px solid #3b5c46;
                gridline-color: #294234;
                color: #d9f99d;
                font-family: "Courier New";
            }

            QHeaderView::section {
                background-color: #1c3325;
                color: #b9ff72;
                border: 1px solid #3b5c46;
                padding: 8px;
                font-weight: bold;
            }

            QProgressBar {
                background-color: #17232d;
                border: 2px solid #3b5c46;
                text-align: center;
                color: #d9f99d;
            }

            QProgressBar::chunk {
                background-color: #6dbb45;
            }

            QFrame#panel {
                background-color: #141f27;
                border: 2px solid #3b5c46;
            }

            QFrame#cpu {
                background-color: #111a20;
                border: 3px solid #6dbb45;
            }
        """)

        self.build_ui()

        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_cpu)

        self.cpu_value = 0
        self.cpu_direction = 1

    # ---------------------------------------------------------
    # BUILD UI
    # ---------------------------------------------------------

    def build_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel("╔════════════════════════════════════════════════════╗")
        subtitle = QLabel("║          PIXEL CPU // PROCESS MANAGER             ║")
        bottom = QLabel("╚════════════════════════════════════════════════════╝")

        title.setAlignment(Qt.AlignCenter)
        subtitle.setAlignment(Qt.AlignCenter)
        bottom.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #b9ff72;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(bottom)

        # =====================================================
        # CPU PANEL
        # =====================================================

        cpu_panel = QFrame()
        cpu_panel.setObjectName("cpu")

        cpu_layout = QVBoxLayout()

        self.cpu_status = QLabel("CPU STATUS: IDLE")
        self.cpu_status.setAlignment(Qt.AlignCenter)

        self.cpu_status.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setValue(0)

        self.cpu_text = QLabel("░░░░░░░░░░░░░░░░░░░░")
        self.cpu_text.setAlignment(Qt.AlignCenter)

        cpu_layout.addWidget(self.cpu_status)
        cpu_layout.addWidget(self.cpu_progress)
        cpu_layout.addWidget(self.cpu_text)

        cpu_panel.setLayout(cpu_layout)

        main_layout.addWidget(cpu_panel)

        # =====================================================
        # INPUT PANEL
        # =====================================================

        input_panel = QFrame()
        input_panel.setObjectName("panel")

        input_layout = QHBoxLayout()

        self.process_input = QLineEdit()
        self.process_input.setPlaceholderText("PROCESS ID  >  P1")

        self.burst_input = QLineEdit()
        self.burst_input.setPlaceholderText("BURST TIME  >  5")

        add_button = QPushButton("[ + ADD PROCESS ]")
        add_button.clicked.connect(self.add_process)

        input_layout.addWidget(self.process_input)
        input_layout.addWidget(self.burst_input)
        input_layout.addWidget(add_button)

        input_panel.setLayout(input_layout)

        main_layout.addWidget(input_panel)

        # =====================================================
        # PROCESS TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "PROCESS",
            "BURST TIME",
            "WAITING TIME",
            "TURNAROUND"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setMinimumHeight(220)

        main_layout.addWidget(self.table)

        # =====================================================
        # BUTTONS
        # =====================================================

        button_layout = QHBoxLayout()

        run_button = QPushButton("▶ RUN SJF")
        run_button.clicked.connect(self.run_sjf)

        clear_button = QPushButton("[ CLEAR ]")
        clear_button.clicked.connect(self.clear_all)

        button_layout.addWidget(run_button)
        button_layout.addWidget(clear_button)

        main_layout.addLayout(button_layout)

        # =====================================================
        # RESULT
        # =====================================================

        self.result_label = QLabel(
            "SJF QUEUE: [ WAITING FOR PROCESSES ]"
        )

        self.result_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
        """)

        main_layout.addWidget(self.result_label)

        # =====================================================
        # GANTT CHART
        # =====================================================

        self.gantt_label = QLabel(
            "GANTT CHART: [ NO SIMULATION ]"
        )

        self.gantt_label.setWordWrap(True)

        self.gantt_label.setStyleSheet("""
            background-color: #111a20;
            border: 2px solid #3b5c46;
            padding: 15px;
            font-size: 16px;
        """)

        main_layout.addWidget(self.gantt_label)

        self.setLayout(main_layout)

    # ---------------------------------------------------------
    # ADD PROCESS
    # ---------------------------------------------------------

    def add_process(self):

        process = self.process_input.text().strip()
        burst = self.burst_input.text().strip()

        if not process or not burst:

            QMessageBox.warning(
                self,
                "INPUT ERROR",
                "ENTER A PROCESS ID AND BURST TIME."
            )

            return

        try:
            burst = int(burst)

            if burst <= 0:
                raise ValueError

        except ValueError:

            QMessageBox.warning(
                self,
                "INPUT ERROR",
                "BURST TIME MUST BE A POSITIVE NUMBER."
            )

            return

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(process)
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(str(burst))
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem("-")
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem("-")
        )

        self.process_input.clear()
        self.burst_input.clear()

        self.result_label.setText(
            "SJF QUEUE: [ NEW PROCESS ADDED ]"
        )

    # ---------------------------------------------------------
    # RUN SJF
    # ---------------------------------------------------------

    def run_sjf(self):

        processes = []

        for row in range(self.table.rowCount()):

            process = self.table.item(row, 0).text()
            burst = int(self.table.item(row, 1).text())

            processes.append(
                [process, burst]
            )

        if not processes:

            QMessageBox.warning(
                self,
                "NO PROCESSES",
                "ADD PROCESSES FIRST."
            )

            return

        # SJF
        processes.sort(
            key=lambda x: x[1]
        )

        current_time = 0

        order = []

        for i, (process, burst) in enumerate(processes):

            waiting_time = current_time

            turnaround_time = waiting_time + burst

            order.append(process)

            current_time += burst

            # Find original process in table
            for row in range(self.table.rowCount()):

                if self.table.item(row, 0).text() == process:

                    self.table.setItem(
                        row,
                        2,
                        QTableWidgetItem(
                            str(waiting_time)
                        )
                    )

                    self.table.setItem(
                        row,
                        3,
                        QTableWidgetItem(
                            str(turnaround_time)
                        )
                    )

                    break

        # Display order

        order_text = "  →  ".join(order)

        self.result_label.setText(
            f"SJF QUEUE:  {order_text}"
        )

        # Create Gantt chart

        self.create_gantt(processes)

        # Start CPU animation

        self.cpu_status.setText(
            "CPU STATUS: PROCESSING..."
        )

        self.animation_timer.start(100)

    # ---------------------------------------------------------
    # GANTT CHART
    # ---------------------------------------------------------

    def create_gantt(self, processes):

        current_time = 0

        chart = ""

        for process, burst in processes:

            chart += (
                f"[ {process} "
                f"{current_time}→"
                f"{current_time + burst} ]  "
            )

            current_time += burst

        self.gantt_label.setText(
            "GANTT CHART:\n\n" + chart
        )

    # ---------------------------------------------------------
    # CPU ANIMATION
    # ---------------------------------------------------------

    def animate_cpu(self):

        self.cpu_value += self.cpu_direction * 5

        if self.cpu_value >= 100:

            self.cpu_direction = -1

        if self.cpu_value <= 20:

            self.cpu_direction = 1

        self.cpu_progress.setValue(
            self.cpu_value
        )

        # Pixel loading animation

        blocks = self.cpu_value // 5

        bar = "█" * blocks
        empty = "░" * (20 - blocks)

        self.cpu_text.setText(
            bar + empty
        )

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------

    def clear_all(self):

        self.table.setRowCount(0)

        self.result_label.setText(
            "SJF QUEUE: [ WAITING FOR PROCESSES ]"
        )

        self.gantt_label.setText(
            "GANTT CHART: [ NO SIMULATION ]"
        )

        self.cpu_progress.setValue(0)

        self.cpu_status.setText(
            "CPU STATUS: IDLE"
        )

        self.animation_timer.stop()


# =============================================================
# APPLICATION
# =============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SJFWindow()

    window.show()

    sys.exit(app.exec())