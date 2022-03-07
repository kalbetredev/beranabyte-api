def update_attributes(updated, existing) -> None:

    for attr, value in updated.__dict__.items():
        if value:
            setattr(existing, attr, value)
