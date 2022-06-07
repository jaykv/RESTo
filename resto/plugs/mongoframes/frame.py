from mongoframes import Frame


class SerializedFrame(Frame):
    @classmethod
    def find_one(cls, filter=None, **kwargs):
        """Return the first document matching the filter"""
        from mongoframes.queries import Condition, Group, to_refs

        # Flatten the projection
        kwargs['projection'], references, subs = cls._flatten_projection(
            kwargs.get('projection', cls._default_projection)
        )

        # Find the document
        if isinstance(filter, (Condition, Group)):
            filter = filter.to_dict()

        document = cls.get_collection().find_one(to_refs(filter), **kwargs)

        # Make sure we found a document
        if not document:
            return

        # Dereference the document (if required)
        if references:
            cls._dereference([document], references)

        # Add sub-frames to the document (if required)
        if subs:
            cls._apply_sub_frames([document], subs)

        return document

    @classmethod
    def find(cls, filter=None, **kwargs):
        """Return a list of serialized documents matching the filter"""
        from mongoframes.queries import Condition, Group, to_refs

        # Flatten the projection
        kwargs['projection'], references, subs = cls._flatten_projection(
            kwargs.get('projection', cls._default_projection)
        )

        # Find the documents
        if isinstance(filter, (Condition, Group)):
            filter = filter.to_dict()

        documents = list(cls.get_collection().find(to_refs(filter), **kwargs))

        # Dereference the documents (if required)
        if references:
            cls._dereference(documents, references)

        # Add sub-frames to the documents (if required)
        if subs:
            cls._apply_sub_frames(documents, subs)

        return documents
