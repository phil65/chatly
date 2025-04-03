"""Thread-related utilities."""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

from prettyqt import core

from chatly.core.translate import _


if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class WorkerSignals(core.Object):
    finished = core.Signal()
    error = core.Signal(Exception)
    result = core.Signal(object)
    progress = core.Signal(int)


class Worker(core.Runnable):
    """Worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn: Callable, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.keyword_args = kwargs
        self.signals = WorkerSignals()
        super().__init__()

        # Add the callback to our kwargs
        # self.keyword_args["progress_callback"] = self.signals.progress

    @core.Slot()
    def run(self):
        """Initialise the runner function with passed args, kwargs."""
        try:
            result = self.fn(*self.args, **self.keyword_args)
            self.signals.result.emit(result)
            self.signals.finished.emit()
        except Exception as e:
            logger.exception("Error running worker.")
            self.signals.error.emit(e)


class GeneratorWorker(Worker):
    @core.Slot()
    def run(self):
        try:
            for result in self.fn(*self.args, **self.keyword_args):
                self.signals.result.emit(result)
            self.signals.finished.emit()
        except Exception as e:
            logger.exception("Error in Worker.")
            self.signals.error.emit(e)


def run_async(func: Callable) -> Callable:
    @functools.wraps(func)
    def async_func(*args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        pool.start(worker)

    return async_func


class ThreadPool(core.ThreadPool):
    """Custom threadpool, manages blocking and non-blocking jobs.

    Emits signals for progressbars in case status changes
    """

    __instance: ThreadPool | None = None
    busy_blocking_on = core.Signal(str)
    busy_blocking_off = core.Signal()
    busy_on = core.Signal()
    busy_off = core.Signal()
    job_num_updated = core.Signal(int)
    exception_occured = core.Signal(Exception)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_jobs = 0
        self.num_jobs_blocking = 0
        self.setMaxThreadCount(4)

    @classmethod
    def instance(cls) -> ThreadPool:
        """Return global ThreadPool singleton instance."""
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def start(  # type: ignore
        self,
        runnable: Worker,
        priority: int = 0,
        set_busy: bool = False,
        message: str | None = None,
    ):
        if set_busy:
            self.num_jobs_blocking += 1
            if self.num_jobs_blocking == 1:
                if not message:
                    message = _("Processing...")
                self.busy_blocking_on.emit(message)
            runnable.signals.finished.connect(self._decrease_num_jobs_blocking)
            runnable.signals.error.connect(self._decrease_num_jobs_blocking)
        else:
            if message:
                core.app().popup_info.emit(message)
            self.num_jobs += 1
            if self.num_jobs == 1:
                self.busy_on.emit()
            runnable.signals.finished.connect(self._decrease_num_jobs)
            runnable.signals.error.connect(self._decrease_num_jobs)
        runnable.signals.error.connect(self.on_exception)
        super().start(runnable, priority)
        self.job_num_updated.emit(self.activeThreadCount())

    def _decrease_num_jobs(self):
        self.num_jobs -= 1
        if self.num_jobs == 0:
            self.busy_off.emit()
        self.job_num_updated.emit(self.activeThreadCount())

    def _decrease_num_jobs_blocking(self):
        self.num_jobs_blocking -= 1
        if self.num_jobs_blocking == 0:
            self.busy_blocking_off.emit()
        self.job_num_updated.emit(self.activeThreadCount())

    def on_exception(self, exception):
        self.exception_occured.emit(exception)


pool = ThreadPool()
